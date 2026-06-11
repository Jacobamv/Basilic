"""Jinja2 templating support.

Kept free of any japronto import so the rendering logic can be unit-tested
without a running server.
"""
from jinja2 import Environment, FileSystemLoader, select_autoescape

__all__ = ["make_environment", "render"]


def make_environment(template_folder):
    """Build a Jinja2 ``Environment`` that loads templates from a folder.

    Autoescaping is enabled for HTML/XML templates by default.
    """
    return Environment(
        loader=FileSystemLoader(template_folder),
        autoescape=select_autoescape(["html", "htm", "xml"]),
    )


def render(environment, template_name, **context):
    """Render ``template_name`` from ``environment`` with the given context."""
    template = environment.get_template(template_name)
    return template.render(**context)
