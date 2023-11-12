import datetime
import decimal
import json
import os
from typing import Any, Callable

from dateutil import parser

EnvVarType = (
    str
    | int
    | float
    | decimal.Decimal
    | bool
    | dict
    | list
    | datetime.date
    | datetime.datetime
)


class RequiredSettingMissing(Exception):
    """Custom error raised when a required env var is missing."""

    def __init__(self, key: str) -> None:
        msg = "Required env var '{}' is missing.".format(key)
        super(RequiredSettingMissing, self).__init__(msg)


class CoercianError(Exception):
    """Custom error raised when a value cannot be coerced."""

    def __init__(self, key: str, value: Any, func: Callable) -> None:
        msg = "Unable to coerce '{}={}' using {}.".format(key, value, func.__name__)
        super(CoercianError, self).__init__(msg)


def _get_env(
    key: str, *, default: EnvVarType | None, coerce: Callable, required: bool
) -> Any:
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
def _bool(value: str) -> bool:
    return value is not None and value.lower() in ("true", "1", "y")


def _int(value: str) -> int:
    return int(value)


def _float(value: str) -> float:
    return float(value)


def _decimal(value: str) -> decimal.Decimal:
    return decimal.Decimal(value)


def _dict(value: str) -> dict:
    return json.loads(value)


def _datetime(value: str) -> datetime.datetime:
    return parser.parse(value)


def _date(value: str) -> datetime.date:
    return parser.parse(value).date()


def get_env(
    key: str, *default: EnvVarType | None, coerce: Callable = lambda x: x
) -> Any:
    """
    Return

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
    if len(default) > 1:
        raise ValueError("Too many args supplied.")
    if len(default) == 0:
        return _get_env(key, default=None, coerce=coerce, required=True)
    return _get_env(key, default=default[0], coerce=coerce, required=False)


def get_bool(key: str, *default: bool) -> bool:
    """Return env var cast as boolean."""
    return get_env(key, *default, coerce=_bool)


def get_int(key: str, *default: int | None) -> int:
    """Return env var cast as integer."""
    return get_env(key, *default, coerce=_int)


def get_float(key: str, *default: float | None) -> float:
    """Return env var cast as float."""
    return get_env(key, *default, coerce=_float)


def get_decimal(key: str, *default: decimal.Decimal | None) -> decimal.Decimal:
    """Return env var cast as Decimal."""
    return get_env(key, *default, coerce=_decimal)


def get_list(key: str, *default: list | None, separator: str = " ") -> list:
    """Return env var as a list."""
    return get_env(key, *default, coerce=lambda x: x.split(separator))


def get_dict(key: str, *default: dict | None) -> dict:
    """Return env var as a dict."""
    return get_env(key, *default, coerce=_dict)


def get_date(key: str, *default: datetime.date | None) -> datetime.date:
    """Return env var as a date."""
    return get_env(key, *default, coerce=_date)


def get_datetime(key: str, *default: datetime.datetime | None) -> datetime.datetime:
    """Return env var as a datetime."""
    return get_env(key, *default, coerce=_datetime)
