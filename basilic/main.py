import functools
import inspect
import mimetypes
import os
import sys

from japronto import Application

from .errors import find_error_handler
from .staticfiles import safe_join
from .templating import make_environment, render

__all__ = ["Basilic"]


def _find_root_path(name):
    """Best-effort absolute root path for the app, based on its import name.

    Mirrors Flask: locate the file of the module named ``name`` and use its
    directory. Falls back to the current working directory.
    """
    module = sys.modules.get(name)
    filename = getattr(module, "__file__", None) if module is not None else None
    if filename:
        return os.path.dirname(os.path.abspath(filename))
    return os.getcwd()


class Basilic(Application):
    """A lightweight, Flask-styled async web framework built on japronto."""

    def __init__(self, name, template_folder="templates",
                 static_folder="static", root_path=None):
        self.name = name
        self.root_path = root_path or _find_root_path(name)
        self.template_folder = template_folder
        self.static_folder = static_folder
        #: Free-form application configuration, like ``flask.Flask.config``.
        self.config = {}
        self.error_handlers = {}
        self._jinja_env = None
        super(Basilic, self).__init__()

    # -- Routing -----------------------------------------------------------

    def route(self, route, methods=None):
        """Register ``func`` as the handler for ``route``.

        Used as a decorator::

            @app.route('/', methods=['GET', 'POST'])
            def handler(request):
                ...

        The decorated function is returned unchanged so it remains callable.
        Handlers are wrapped so that exceptions are dispatched to any matching
        :meth:`errorhandler`.
        """
        if methods is None:
            methods = ["GET"]

        def inner(func):
            self.router.add_route(route, self._wrap_handler(func),
                                  methods=methods)
            return func

        return inner

    # -- Error handling ----------------------------------------------------

    def errorhandler(self, exc_class):
        """Register a handler for exceptions of type ``exc_class``.

        Used as a decorator. The handler is called as ``handler(request, exc)``
        and must return a response synchronously::

            @app.errorhandler(ValueError)
            def on_value_error(request, exc):
                return request.Response(code=400, text=str(exc))

        A handler registered for a base class also catches its subclasses.
        """
        def inner(func):
            self.error_handlers[exc_class] = func
            return func

        return inner

    def _handle_exception(self, request, exc):
        handler = find_error_handler(self.error_handlers, type(exc))
        if handler is None:
            raise exc
        return handler(request, exc)

    def _wrap_handler(self, func):
        """Wrap a route handler so raised exceptions hit the error handlers.

        Preserves whether the handler is a coroutine so japronto still treats
        async handlers correctly.
        """
        if inspect.iscoroutinefunction(func):
            @functools.wraps(func)
            async def wrapper(request):
                try:
                    return await func(request)
                except Exception as exc:  # noqa: BLE001 - dispatched below
                    return self._handle_exception(request, exc)
        else:
            @functools.wraps(func)
            def wrapper(request):
                try:
                    return func(request)
                except Exception as exc:  # noqa: BLE001 - dispatched below
                    return self._handle_exception(request, exc)
        return wrapper

    # -- Templating --------------------------------------------------------

    @property
    def jinja_env(self):
        """Lazily-built Jinja2 environment rooted at the template folder."""
        if self._jinja_env is None:
            path = os.path.join(self.root_path, self.template_folder)
            self._jinja_env = make_environment(path)
        return self._jinja_env

    def render_template(self, request, template_name, **context):
        """Render a template to an ``text/html`` response.

        ::

            @app.route('/')
            def index(request):
                return app.render_template(request, 'index.html', name='World')
        """
        html = render(self.jinja_env, template_name, **context)
        return request.Response(text=html, mime_type="text/html")

    # -- Static files ------------------------------------------------------

    def add_static_route(self, url_prefix="/static", static_folder=None):
        """Register a route that serves files from ``static_folder``.

        ``url_prefix`` is the URL mount point (default ``/static``); files are
        read from ``static_folder`` (default ``<root_path>/<static_folder>``).
        Path traversal outside the folder is rejected with 403.
        """
        folder = static_folder or os.path.join(self.root_path,
                                                self.static_folder)
        route = url_prefix.rstrip("/") + "/{filename}"

        def handler(request):
            filename = request.match_dict["filename"]
            return self._serve_static(request, folder, filename)

        self.router.add_route(route, handler, methods=["GET"])

    @staticmethod
    def _serve_static(request, folder, filename):
        target = safe_join(folder, filename)
        if target is None:
            return request.Response(code=403, text="Forbidden")
        if not os.path.isfile(target):
            return request.Response(code=404, text="Not Found")
        with open(target, "rb") as fh:
            data = fh.read()
        mime = mimetypes.guess_type(target)[0] or "application/octet-stream"
        return request.Response(body=data, mime_type=mime)
