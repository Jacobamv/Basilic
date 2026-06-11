"""Shared test helpers.

Importing the ``basilic`` package runs ``basilic/__init__.py``, which imports
japronto. japronto only builds on POSIX systems, so on Windows (and any host
without it installed) that import fails. The pure helpers (``jsonify``,
``templating``) don't need japronto, so we load those module files directly,
bypassing the package ``__init__``. Tests that exercise the japronto-backed
``Basilic`` app use ``pytest.importorskip("japronto")`` instead.
"""
import importlib.util
import pathlib

BASILIC_DIR = pathlib.Path(__file__).resolve().parent.parent / "basilic"


def load_module(filename, name=None):
    """Load ``basilic/<filename>`` directly from its file path."""
    path = BASILIC_DIR / filename
    module_name = name or "basilic_" + path.stem
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FakeRequest:
    """Minimal stand-in for a japronto Request.

    ``Response`` records the keyword arguments it was called with so tests can
    assert on what a handler/helper produced without a running server.
    """

    def Response(self, **kwargs):
        return kwargs
