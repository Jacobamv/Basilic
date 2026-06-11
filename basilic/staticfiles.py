"""Helpers for serving static files safely.

Kept free of any japronto import so the path-safety logic can be unit-tested
without a running server.
"""
import os

__all__ = ["safe_join"]


def safe_join(directory, filename):
    """Resolve ``filename`` inside ``directory``, guarding against traversal.

    Returns the absolute path to the target if it stays within ``directory``,
    otherwise ``None`` (e.g. for ``../`` escapes, absolute paths, or — on
    Windows — a different drive). This does not check that the file exists.
    """
    directory_abs = os.path.abspath(directory)
    target = os.path.abspath(os.path.join(directory_abs, filename))
    try:
        common = os.path.commonpath([directory_abs, target])
    except ValueError:
        # Raised when paths are on different drives (Windows) or mix
        # absolute/relative — treat as unsafe.
        return None
    if common != directory_abs:
        return None
    return target
