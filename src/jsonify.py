def jsonify(request, *args, **kwargs):
    js = {}
    for i in args:
        js.update(i)
    js.update(kwargs)
    return request.Response(json=js)
