# -*- coding: utf-8 -*-
"""env_utils package declaration."""
import os
from past.builtins import basestring


def to_bool(value):
    """Coerce string value into a boolean.

    Python evaluates any string as True, which isn't the desired behaviour
    when setting environment variables. Ideally "0" and "False" would
    evaluate to False.
    """
    if value is None:
        return False
    if isinstance(value, bool):
        return value
    if isinstance(value, basestring):
        return value.lower() in ("true", "1")
    raise ValueError("Unparseable value: %s" % value)


def to_int(value):
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


def get_bool(key, default):
    """Get environ value as bool."""
    assert default is not None, u"Default value cannot be None."
    assert isinstance(default, bool), u"Invalid bool default: %s" % default
    return getenv(key, default=default, coerce=to_bool)


def get_int(key, default):
    """Get environ value as integer."""
    assert default is not None, u"Default value cannot be None."
    assert isinstance(default, int), u"Invalid int default: %s" % default
    return getenv(key, default=default, coerce=to_int)
