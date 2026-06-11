from conftest import load_module

find_error_handler = load_module("errors.py").find_error_handler


def _h(label):
    def handler(request, exc):
        return label
    return handler


def test_exact_match():
    handler = _h("v")
    assert find_error_handler({ValueError: handler}, ValueError) is handler


def test_subclass_matched_via_base():
    handler = _h("base")
    # ValueError is not registered, but its base Exception is.
    assert find_error_handler({Exception: handler}, ValueError) is handler


def test_most_specific_wins():
    base, specific = _h("base"), _h("specific")
    handlers = {Exception: base, ValueError: specific}
    assert find_error_handler(handlers, ValueError) is specific


def test_no_match_returns_none():
    assert find_error_handler({KeyError: _h("k")}, ValueError) is None
