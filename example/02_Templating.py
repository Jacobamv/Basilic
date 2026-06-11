"""Render a Jinja2 template.

Templates are loaded from the ``templates/`` folder next to this file.
Run with:  python example/02_Templating.py
"""
from basilic import Basilic

app = Basilic(__name__)


@app.route("/")
def index(request):
    return app.render_template(request, "index.html", name="World")


app.run()
