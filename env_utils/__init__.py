# -*- coding: utf-8 -*-
"""env_utils package declaration."""
import os


def bool_(value):
    """Coerce string value into a boolean.

    Python evaluates any string as True, which isn't the desired behaviour
    when setting environment variables. Ideally "0" and "False" would
    evaluate to False.
    """
    assert isinstance(value, basestring)
    return value.lower() in ("true", "1")


def int_(value):
    """Coerce string value into an integer."""
    assert isinstance(value, basestring)
    return int(value)


def getenv(key, default=None, coerce=lambda x: x):
    """Return env var coerced into a type other than string.

    This function extends the standard os.getenv function to enable
    the coercion of values into data types other than string (all env
    vars are strings be default).

    e.g., coerce the value into an int, use coerce=lambda x: int(x).

    """
    return coerce(os.getenv(key, default))
