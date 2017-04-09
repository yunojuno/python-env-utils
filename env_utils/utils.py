# -*- coding: utf-8 -*-
import decimal
import json
import os

from dateutil import parser


class RequiredSettingMissing(Exception):

    """Custom error raised when a required env var is missing."""

    def __init__(self, key):
        msg = "Required env var '{}' is missing.".format(key)
        super(RequiredSettingMissing, self).__init__(msg)


class CoercianError(Exception):

    """Custom error raised when a value cannot be coerced."""

    def __init__(self, key, value, func):
        msg = "Unable to coerce '{}={}' using {}.".format(key, value, func.__name__)
        super(CoercianError, self).__init__(msg)


def _get_env(key, default=None, coerce=lambda x: x, required=False):
    """
    Return env var coerced into a type other than string.

    This function extends the standard os.getenv function to enable
    the coercion of values into data types other than string (all env
    vars are strings by default).

    Args:
        key: string, the name of the env var to look up

    Kwargs:
        default: the default value to return if the env var does not exist. NB the
            default value is **not** coerced, and is assumed to be of the correct type.
        coerce: a function that is used to coerce the value returned into
            another type
        required: bool, if True, then a RequiredSettingMissing error is raised
            if the env var does not exist.

    Returns the env var, passed through the coerce function

    """
    try:
        value = os.environ[key]
    except KeyError:
        if required is True:
            raise RequiredSettingMissing(key)
        else:
            return default

    try:
        return coerce(value)
    except Exception:
        raise CoercianError(key, value, coerce)


# standard type coercian functions
def _bool(value):
    if isinstance(value, bool):
        return value
    return value is not None and value.lower() in ("true", "1", "y")


def _int(value):
    return int(value)


def _float(value):
    return float(value)


def _decimal(value):
    return decimal.Decimal(value)


def _dict(value):
    return json.loads(value)


def _datetime(value):
    return parser.parse(value)


def _date(value):
    return parser.parse(value).date()


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
    return get_env(key, *default, coerce=_bool)


def get_int(key, *default):
    """Return env var cast as integer."""
    return get_env(key, *default, coerce=_int)


def get_float(key, *default):
    """Return env var cast as float."""
    return get_env(key, *default, coerce=_float)


def get_decimal(key, *default):
    """Return env var cast as Decimal."""
    return get_env(key, *default, coerce=_decimal)


def get_list(key, *default, **kwargs):
    """Return env var as a list."""
    separator = kwargs.get('separator', ' ')
    return get_env(key, *default, coerce=lambda x: x.split(separator))


def get_dict(key, *default):
    """Return env var as a dict."""
    return get_env(key, *default, coerce=_dict)


def get_date(key, *default):
    """Return env var as a date."""
    return get_env(key, *default, coerce=_date)


def get_datetime(key, *default):
    """Return env var as a datetime."""
    return get_env(key, *default, coerce=_datetime)
