"""Serve static files from the ``static/`` folder next to this file.

After running, fetch e.g.  http://localhost:8080/static/style.css
Run with:  python example/03_Static_Files.py
"""
from basilic import Basilic

app = Basilic(__name__)

# Mounts <this folder>/static at the /static URL prefix.
app.add_static_route("/static")


@app.route("/")
def index(request):
    return request.Response(
        text='<link rel="stylesheet" href="/static/style.css"><h1>Styled!</h1>',
        mime_type="text/html",
    )


app.run()
