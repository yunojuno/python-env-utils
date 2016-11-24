# -*- coding: utf-8 -*-
from dateutil import parser
import decimal
import json
import os


class RequiredSettingMissing(Exception):

    def __init__(self, key):
        msg = u"Required env var '%s' is missing." % key
        super(RequiredSettingMissing, self).__init__(msg)


def _get_env(key, default=None, coerce=lambda x: x, required=False):
    """Return env var coerced into a type other than string.

    This function extends the standard os.getenv function to enable
    the coercion of values into data types other than string (all env
    vars are strings be default).

    Args:
        key: string, the name of the env var to look up

    Kwargs:
        default: the default value to return if the env var does not exist
        coerce: a function that is used to coerce the value returned into
            another type
        required: bool, if True, then a RequiredSettingMissing error is raised
            if the env var does not exist.

    Returns the env var, passed through the coerce function

    """
    try:
        return coerce(os.environ[key])
    except KeyError:
        if required is True:
            raise RequiredSettingMissing(key)
        else:
            return default


# standard type coercian functions
coerce_bool = lambda x: x is not None and x.lower() in ("true", "1", "y")
coerce_int = lambda x: int(x)
coerce_float = lambda x: float(x)
coerce_decimal = lambda x: decimal.Decimal(x)
coerce_dict = lambda x: json.loads(x)
coerce_datetime = lambda x: parser.parse(x)
coerce_date = lambda x: parser.parse(x).date()


def get_env(key, *default, **kwargs):
    """
    Return env var.

    This is the parent function of all other get_foo functions,
    and is responsible for unpacking args/kwargs into the values
    that _get_env expects (it is the root function that actually
    interacts with environ).

    Args:
        key: string, the env var name to look up.
        default: (optional) the value to use if the env var does not
            exist. If this value is not supplied, then the env var is
            considered to be required, and a RequiredSettingMissing
            error will be raised if it does not exist.

    Kwargs:
        coerce: a func that may be supplied to coerce the value into
            something else. This is used by the default get_foo functions
            to cast strings to builtin types, but could be a function that
            returns a custom class.

    Returns the env var, coerced if required, and a default if supplied.

    """
    assert len(default) in (0, 1), "Too many args supplied."
    func = kwargs.get('coerce', lambda x: x)
    required = (len(default) == 0)
    default = default[0] if not required else None
    return _get_env(key, default=default, coerce=func, required=required)


def get_bool(key, *default):
    """Return env var cast as boolean."""
    return get_env(key, *default, coerce=coerce_bool)


def get_int(key, *default):
    """Return env var cast as integer."""
    return get_env(key, *default, coerce=coerce_int)


def get_float(key, *default):
    """Return env var cast as float."""
    return get_env(key, *default, coerce=coerce_float)


def get_decimal(key, *default):
    """Return env var cast as Decimal."""
    return get_env(key, *default, coerce=coerce_decimal)


def get_list(key, *default, **kwargs):
    """Return env var as a list."""
    separator = kwargs.get('separator', ' ')
    func = lambda x: x.split(separator)
    return get_env(key, *default, coerce=func)


def get_dict(key, *default):
    """Return env var as a dict."""
    return get_env(key, *default, coerce=coerce_dict)


def get_date(key, *default):
    """Return env var as a date."""
    return get_env(key, *default, coerce=coerce_date)


def get_datetime(key, *default):
    """Return env var as a datetime."""
    return get_env(key, *default, coerce=coerce_datetime)
