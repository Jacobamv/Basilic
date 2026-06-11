import os

from conftest import load_module

safe_join = load_module("staticfiles.py").safe_join


def test_normal_file(tmp_path):
    target = safe_join(str(tmp_path), "a.txt")
    assert target is not None
    assert os.path.basename(target) == "a.txt"
    assert target.startswith(os.path.abspath(str(tmp_path)))


def test_subdirectory(tmp_path):
    target = safe_join(str(tmp_path), os.path.join("sub", "a.txt"))
    assert target is not None
    assert target.startswith(os.path.abspath(str(tmp_path)))


def test_parent_traversal_blocked(tmp_path):
    assert safe_join(str(tmp_path), "../secret.txt") is None
    assert safe_join(str(tmp_path), os.path.join("..", "..", "etc", "passwd")) is None


def test_absolute_path_blocked(tmp_path):
    absolute = os.path.abspath(os.path.join(os.sep, "etc", "passwd"))
    assert safe_join(str(tmp_path), absolute) is None
