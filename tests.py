import datetime
import inspect
import unittest
from decimal import Decimal, InvalidOperation
from typing import Any, Callable
from unittest import mock

from env_utils.utils import (
    CoercianError,
    RequiredSettingMissing,
    _bool,
    _date,
    _datetime,
    _decimal,
    _dict,
    _float,
    _get_env,
    _int,
    get_bool,
    get_date,
    get_datetime,
    get_decimal,
    get_dict,
    get_env,
    get_float,
    get_int,
    get_list,
)


class TestFunctions(unittest.TestCase):
    """Basic function tests."""

    def assertFunc(self, func: Callable, value: Any, expected: Any) -> None:
        with mock.patch.dict("os.environ", {"foo": value}):
            if inspect.isclass(expected):
                self.assertRaises(expected, func, "foo")
            else:
                self.assertEqual(func("foo"), expected)

    def test__bool(self) -> None:
        self.assertEqual(_bool("true"), True)
        self.assertEqual(_bool("TRUE"), True)
        self.assertEqual(_bool("1"), True)
        self.assertEqual(_bool("y"), True)
        self.assertEqual(_bool("tru"), False)
        self.assertEqual(_bool("0"), False)

    def test__int(self) -> None:
        self.assertEqual(_int("01"), 1)
        self.assertRaises(ValueError, _int, "foo")

    def test__float(self) -> None:
        self.assertEqual(_float("01"), 1.0)
        self.assertRaises(ValueError, _float, "foo")

    def test__decimal(self) -> None:
        self.assertEqual(_decimal("01"), Decimal("1.0"))
        self.assertRaises(InvalidOperation, _decimal, "foo")

    def test__dict(self) -> None:
        self.assertEqual(_dict("false"), False)
        self.assertEqual(_dict('{"foo": false}'), {"foo": False})
        self.assertRaises(ValueError, _dict, "hello, world!")

    def test__datetime(self) -> None:
        now = datetime.datetime.now()
        self.assertEqual(_datetime(now.isoformat()), now)
        # add timezone info
        now = datetime.datetime.now(datetime.timezone.utc)
        self.assertEqual(_datetime(now.isoformat()), now)
        self.assertRaises(ValueError, _datetime, "hello, world!")

    def test__date(self) -> None:
        today = datetime.date.today()
        self.assertEqual(_date(today.isoformat()), today)
        # add timezone info
        self.assertRaises(ValueError, _date, "hello, world!")

    def test__get_env(self) -> None:
        # env var is missing
        self.assertRaises(
            RequiredSettingMissing,
            _get_env,
            "FOO",
            default=None,
            coerce=lambda x: x,
            required=True,
        )
        self.assertEqual(
            _get_env("bar", default="baz", coerce=lambda x: x, required=False), "baz"
        )
        # env var exists
        with mock.patch.dict("os.environ", {"FOO": "bar"}):
            self.assertEqual(
                _get_env("FOO", default=None, coerce=lambda x: x, required=False), "bar"
            )
            # env var coercian fails
            self.assertRaises(
                Exception,
                _get_env,
                "FOO",
                default=None,
                coerce=(lambda x: int(x)),
                required=False,
            )

    def test__get_env_defaults(self) -> None:
        # test default values are **not** coerced
        self.assertEqual(
            _get_env("FOO", default="1", coerce=lambda x: int(x), required=False), "1"
        )

    def test_get_env(self) -> None:
        # too many args - we only support one default value ('bar')
        self.assertRaises(ValueError, get_env, "foo", "bar", "baz")
        # missing env var, use default
        self.assertRaises(RequiredSettingMissing, get_env, "FOO", coerce=(lambda x: x))
        self.assertEqual(get_env("FOO", "bar", coerce=lambda x: x), "bar")
        # valid env var
        self.assertFunc(get_env, "foo", "foo")

    def test_get_bool(self) -> None:
        self.assertFunc(get_bool, "bar", False)
        self.assertFunc(get_bool, "1", True)

    def test_get_int(self) -> None:
        self.assertFunc(get_int, "1", 1)
        self.assertFunc(get_int, "bar", CoercianError)

    def test_get_float(self) -> None:
        self.assertFunc(get_float, "1.0", 1.0)
        self.assertFunc(get_float, "bar", CoercianError)

    def test_get_decimal(self) -> None:
        self.assertFunc(get_decimal, "1", Decimal("1"))
        self.assertFunc(get_decimal, "bar", CoercianError)

    def test_get_list(self) -> None:
        self.assertFunc(get_list, "false", ["false"])
        self.assertFunc(get_list, "true false", ["true", "false"])
        with mock.patch.dict("os.environ", {"foo": "true,false"}):
            # self.environ['foo'] = "true,false"
            self.assertEqual(get_list("foo", separator=","), ["true", "false"])
            self.assertEqual(get_list("foo", ["baz"]), ["true,false"])

    def test_get_dict(self) -> None:
        self.assertFunc(get_dict, "false", False)
        self.assertFunc(get_dict, '{"foo": false}', {"foo": False})
        self.assertFunc(get_dict, "hello, world!", CoercianError)

    def test_get_date(self) -> None:
        self.assertFunc(get_date, "2016-11-23", datetime.date(2016, 11, 23))
        self.assertFunc(get_date, "hello, world!", CoercianError)

        # get_date also supports other date formats
        with mock.patch.dict("os.environ", {"foo": "23-11-2016"}):
            self.assertEqual(get_date("foo"), datetime.date(2016, 11, 23))

    def test_get_datetime(self) -> None:
        now = datetime.datetime.now()
        self.assertFunc(get_datetime, now.isoformat(), now)
        # add timezone info
        now = datetime.datetime.now(datetime.timezone.utc)
        self.assertFunc(get_datetime, now.isoformat(), now)
        self.assertFunc(get_datetime, "hello, world!", CoercianError)


if __name__ == "__main__":
    unittest.main()
