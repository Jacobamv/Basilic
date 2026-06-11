# Basilic

**Basilic** is a lightweight, asynchronous web framework for Python, styled
after [Flask](https://flask.palletsprojects.com/) and built on top of the
high-performance [japronto](https://github.com/squeaky-pl/japronto) HTTP server.
It aims to give you Flask's familiar, decorator-based API with async speed
underneath.

> ⚠️ **Platform:** japronto only builds on **macOS / Linux / *nix**. Basilic
> does not run on Windows (use WSL or a Linux container there).

## Installation

```bash
pip install basilic
```

Or from source:

```bash
git clone https://github.com/Jacobamv/Basilic
cd Basilic
pip install .
```

Requires Python 3.5+ (the framework is async-only). Dependencies: `japronto`,
`jinja2`.

## Quick start

```python
from basilic import Basilic, jsonify

app = Basilic(__name__)

@app.route('/')
def index(request):
    return jsonify(request, msg="HelloWorld")

app.run()
```

```bash
python app.py   # serves on http://0.0.0.0:8080
```

## Features

### Routing

Register handlers with the `@app.route` decorator. The decorated function is
returned unchanged, so it stays callable.

```python
@app.route('/submit', methods=['GET', 'POST'])
def submit(request):
    return request.Response(text="ok")
```

### JSON responses

`jsonify` merges any number of dicts plus keyword arguments into a single JSON
response. Keyword arguments win on conflict.

```python
@app.route('/api')
def api(request):
    return jsonify(request, {"status": "ok"}, count=3)
    # -> {"status": "ok", "count": 3}
```

### Templating (Jinja2)

Templates are loaded from a `templates/` folder next to your application module.
Autoescaping is enabled for HTML by default.

```python
@app.route('/')
def index(request):
    return app.render_template(request, 'index.html', name='World')
```

```
your_app.py
templates/
└── index.html      # <h1>Hello {{ name }}!</h1>
```

You can override the folder: `Basilic(__name__, template_folder='views')`.

### Static files

Mount a folder of static assets at a URL prefix. Path traversal outside the
folder is rejected with `403`.

```python
app.add_static_route('/static')   # serves <root>/static/* at /static/*
```

### Error handlers

Catch exceptions raised inside handlers and turn them into responses. A handler
registered for a base class also catches its subclasses.

```python
@app.errorhandler(ValueError)
def on_value_error(request, exc):
    return request.Response(code=400, text=str(exc))
```

Error handlers run synchronously and must return a response. Unhandled
exceptions propagate to japronto.

### Configuration

Each app has a free-form `config` dict, like Flask's:

```python
app.config['DEBUG'] = True
```

## Examples

See the [`example/`](example/) folder:

| File | Shows |
| --- | --- |
| `01_Hello_World.py` | Minimal JSON app |
| `02_Templating.py` | Jinja2 templates |
| `03_Static_Files.py` | Serving static assets |
| `04_Error_Handling.py` | `@app.errorhandler` |

## Development & tests

```bash
pip install -e .[test]
pytest
```

The pure helpers (`jsonify`, templating, static-path safety, error matching)
are tested on any platform. Tests that exercise the japronto-backed app are
skipped automatically where japronto isn't installed (e.g. Windows).

## License

GPL-2.0-or-later. See [LICENSE](LICENSE).
