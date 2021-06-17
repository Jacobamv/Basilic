from basilic import Basilic, jsonify


app = Basilic(__name__)


@app.route('/')
def Something(request):
    return jsonify(request,msg="HelloWorld")


app.run()