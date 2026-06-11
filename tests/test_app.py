import pytest

# These exercise the Basilic app object, which subclasses japronto.Application
# and therefore requires japronto. Skip cleanly where it isn't installed.
pytest.importorskip("japronto")

from basilic import Basilic  # noqa: E402
from conftest import FakeRequest  # noqa: E402


def test_config_is_per_instance():
    a, b = Basilic(__name__), Basilic(__name__)
    a.config["DEBUG"] = True
    assert b.config == {}


def test_errorhandler_dispatch():
    app = Basilic(__name__)

    @app.errorhandler(ValueError)
    def on_err(request, exc):
        return request.Response(code=400, text=str(exc))

    def handler(request):
        raise ValueError("boom")

    wrapped = app._wrap_handler(handler)
    assert wrapped(FakeRequest()) == {"code": 400, "text": "boom"}


def test_errorhandler_catches_subclass():
    app = Basilic(__name__)

    @app.errorhandler(Exception)
    def on_err(request, exc):
        return request.Response(code=500, text="handled")

    def handler(request):
        raise ValueError("boom")

    assert app._wrap_handler(handler)(FakeRequest())["text"] == "handled"


def test_unhandled_exception_reraises():
    app = Basilic(__name__)

    def handler(request):
        raise KeyError("x")

    with pytest.raises(KeyError):
        app._wrap_handler(handler)(FakeRequest())


def test_wrap_preserves_coroutine():
    import inspect

    app = Basilic(__name__)

    async def handler(request):
        return "ok"

    assert inspect.iscoroutinefunction(app._wrap_handler(handler))


def test_serve_static_ok(tmp_path):
    (tmp_path / "a.txt").write_text("hi")
    result = Basilic._serve_static(FakeRequest(), str(tmp_path), "a.txt")
    assert result["body"] == b"hi"
    assert result["mime_type"] == "text/plain"


def test_serve_static_traversal_forbidden(tmp_path):
    result = Basilic._serve_static(FakeRequest(), str(tmp_path), "../secret")
    assert result == {"code": 403, "text": "Forbidden"}


def test_serve_static_missing(tmp_path):
    result = Basilic._serve_static(FakeRequest(), str(tmp_path), "nope.txt")
    assert result == {"code": 404, "text": "Not Found"}
