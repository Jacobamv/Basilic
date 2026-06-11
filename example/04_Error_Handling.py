"""Catch exceptions raised in handlers with @app.errorhandler.

Run with:  python example/04_Error_Handling.py
Then visit /  -> 400 response produced by the error handler.
"""
from basilic import Basilic

app = Basilic(__name__)


@app.errorhandler(ValueError)
def on_value_error(request, exc):
    return request.Response(code=400, text="Bad value: {}".format(exc))


@app.route("/")
def index(request):
    raise ValueError("something went wrong")


app.run()
