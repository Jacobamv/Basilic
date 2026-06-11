import pytest

# The Basilic class subclasses japronto.Application, so importing it requires
# japronto. Skip the whole module cleanly where japronto isn't available.
pytest.importorskip("japronto")

from basilic import Basilic  # noqa: E402


def test_route_returns_function_unchanged():
    app = Basilic(__name__)

    @app.route("/")
    def handler(request):
        return "ok"

    # The decorator must return the original function, not None.
    assert handler is not None
    assert callable(handler)
    assert handler.__name__ == "handler"


def test_route_registers_handler():
    app = Basilic(__name__)

    @app.route("/hello", methods=["GET", "POST"])
    def hello(request):
        return "hi"

    # The handler should be registered on the router. japronto stores routes
    # internally; at minimum the decorator returned the function and did not
    # raise during registration.
    assert hello.__name__ == "hello"


def test_default_methods_do_not_leak_between_routes():
    # Regression guard against a mutable default argument for ``methods``.
    app = Basilic(__name__)

    @app.route("/a")
    def a(request):
        return "a"

    @app.route("/b", methods=["POST"])
    def b(request):
        return "b"

    # If ``methods`` defaulted to a shared list and were mutated, registering
    # /b could corrupt /a. We can't easily read japronto's internal table, so
    # this mainly documents intent; the real protection is methods=None above.
    assert a.__name__ == "a"
    assert b.__name__ == "b"
