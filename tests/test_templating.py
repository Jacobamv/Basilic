from conftest import load_module

templating = load_module("templating.py")


def test_render_simple(tmp_path):
    (tmp_path / "hello.html").write_text("Hello {{ name }}!")
    env = templating.make_environment(str(tmp_path))
    assert templating.render(env, "hello.html", name="World") == "Hello World!"


def test_autoescape_html(tmp_path):
    (tmp_path / "x.html").write_text("{{ val }}")
    env = templating.make_environment(str(tmp_path))
    out = templating.render(env, "x.html", val="<script>")
    assert "&lt;script&gt;" in out
    assert "<script>" not in out
