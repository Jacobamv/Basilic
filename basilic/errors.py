"""Error-handler lookup.

Kept free of any japronto import so the matching logic can be unit-tested
without a running server.
"""

__all__ = ["find_error_handler"]


def find_error_handler(handlers, exc_type):
    """Find the most specific handler in ``handlers`` for ``exc_type``.

    ``handlers`` maps exception classes to callables. The exception's MRO is
    walked from most to least specific, so a handler registered for a base
    class also catches its subclasses. Returns ``None`` if nothing matches.
    """
    for klass in exc_type.__mro__:
        if klass in handlers:
            return handlers[klass]
    return None
