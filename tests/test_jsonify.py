from conftest import FakeRequest, load_module

jsonify = load_module("jsonify.py").jsonify


def test_empty():
    result = jsonify(FakeRequest())
    assert result == {"json": {}}


def test_kwargs_only():
    result = jsonify(FakeRequest(), msg="HelloWorld", n=1)
    assert result["json"] == {"msg": "HelloWorld", "n": 1}


def test_single_dict_arg():
    result = jsonify(FakeRequest(), {"a": 1, "b": 2})
    assert result["json"] == {"a": 1, "b": 2}


def test_multiple_dicts_merge():
    result = jsonify(FakeRequest(), {"a": 1}, {"b": 2})
    assert result["json"] == {"a": 1, "b": 2}


def test_kwargs_override_dict():
    # kwargs are applied after positional dicts, so they win on conflict.
    result = jsonify(FakeRequest(), {"a": 1}, a=2)
    assert result["json"] == {"a": 2}


def test_later_dict_overrides_earlier():
    result = jsonify(FakeRequest(), {"a": 1}, {"a": 2})
    assert result["json"] == {"a": 2}
