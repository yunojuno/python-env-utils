# -*- coding: utf-8 -*-
import datetime
from decimal import Decimal, InvalidOperation
import inspect

import pytz
import unittest

from .compat import mock
from .utils import (
    get_env,
    get_bool,
    get_int,
    get_float,
    get_decimal,
    get_list,
    get_dict,
    get_date,
    get_datetime,
    _get_env,
    RequiredSettingMissing,
    CoercianError,
    _bool,
    _int,
    _float,
    _decimal,
    _dict,
    _datetime,
    _date,
)


class TestFunctions(unittest.TestCase):

    """Basic function tests."""

    def assertFunc(self, func, value, expected):
        with mock.patch.dict('os.environ', {'foo': value}):
            if inspect.isclass(expected):
                self.assertRaises(expected, func, 'foo')
            else:
                self.assertEqual(func("foo"), expected)

    def test__bool(self):
        self.assertEqual(_bool("true"), True)
        self.assertEqual(_bool("TRUE"), True)
        self.assertEqual(_bool("1"), True)
        self.assertEqual(_bool("y"), True)
        self.assertEqual(_bool("tru"), False)
        self.assertEqual(_bool("0"), False)
        self.assertEqual(_bool(None), False)
        self.assertEqual(_bool(True), True)
        self.assertEqual(_bool(False), False)

    def test__int(self):
        self.assertEqual(_int("01"), 1)
        self.assertEqual(_int(1), 1)
        self.assertRaises(ValueError, _int, "foo")

    def test__float(self):
        self.assertEqual(_float("01"), 1.0)
        self.assertEqual(_float(1), 1.0)
        self.assertEqual(_float(1.0), 1.0)
        self.assertRaises(ValueError, _float, "foo")

    def test__decimal(self):
        self.assertEqual(_decimal("01"), Decimal('1.0'))
        self.assertEqual(_decimal(1), Decimal('1.0'))
        self.assertEqual(_decimal(1.0), Decimal('1.0'))
        self.assertRaises(InvalidOperation, _decimal, "foo")

    def test__dict(self):
        self.assertEqual(_dict("false"), False)
        self.assertEqual(_dict("{\"foo\": false}"), {'foo': False})
        self.assertRaises(ValueError, _dict, "hello, world!")

    def test__datetime(self):
        now = datetime.datetime.now()
        self.assertEqual(_datetime(now.isoformat()), now)
        # add timezone info
        now = datetime.datetime.now(pytz.utc)
        self.assertEqual(_datetime(now.isoformat()), now)
        self.assertRaises(ValueError, _datetime, "hello, world!")

    def test__date(self):
        today = datetime.date.today()
        self.assertEqual(_date(today.isoformat()), today)
        # add timezone info
        self.assertRaises(ValueError, _date, "hello, world!")

    def test__get_env(self):
        # env var is missing
        self.assertRaises(
            RequiredSettingMissing,
            _get_env,
            'FOO',
            required=True
        )
        self.assertEqual(_get_env("bar", 'baz'), 'baz')
        # env var exists
        with mock.patch.dict('os.environ', {'FOO': 'bar'}):
            self.assertEqual(_get_env('FOO', None), 'bar')
            # env var coercian fails
            self.assertRaises(
                Exception,
                _get_env,
                "FOO",
                coerce=(lambda x: int(x))
            )

    def test__get_env_defaults(self):
        # test default values are **not** coerced
        self.assertEqual(_get_env('FOO', '1', coerce=lambda x: int(x)), '1')

    def test_get_env(self):
        # too many args - we only support one default value ('bar')
        self.assertRaises(AssertionError, get_env, 'foo', 'bar', 'baz')
        # missing env var, use default
        self.assertRaises(RequiredSettingMissing, get_env, 'FOO', coerce=(lambda x: x))
        self.assertEqual(get_env('FOO', 'bar', coerce=lambda x: x), 'bar')
        # valid env var
        self.assertFunc(get_env, 'foo', 'foo')

    def test_get_bool(self):
        self.assertFunc(get_bool, "bar", False)
        self.assertFunc(get_bool, "1", True)

    def test_get_int(self):
        self.assertFunc(get_int, "1", 1)
        self.assertFunc(get_int, "bar", CoercianError)

    def test_get_float(self):
        self.assertFunc(get_float, "1.0", 1.0)
        self.assertFunc(get_float, "bar", CoercianError)

    def test_get_decimal(self):
        self.assertFunc(get_decimal, "1", Decimal("1"))
        self.assertFunc(get_decimal, "bar", CoercianError)

    def test_get_list(self):
        self.assertFunc(get_list, "false", ['false'])
        self.assertFunc(get_list, "true false", ['true', 'false'])
        with mock.patch.dict('os.environ', {'foo': 'true,false'}):
            # self.environ['foo'] = "true,false"
            self.assertEqual(get_list('foo', separator=','), ['true', 'false'])
            self.assertEqual(get_list('foo', ["baz"]), ['true,false'])

    def test_get_dict(self):
        self.assertFunc(get_dict, "false", False)
        self.assertFunc(get_dict, "{\"foo\": false}", {'foo': False})
        self.assertFunc(get_dict, "hello, world!", CoercianError)

    def test_get_date(self):
        self.assertFunc(get_date, "2016-11-23", datetime.date(2016, 11, 23))
        self.assertFunc(get_date, "hello, world!", CoercianError)

        # get_date also supports other date formats
        with mock.patch.dict('os.environ', {'foo': '23-11-2016'}):
            self.assertEqual(get_date("foo"), datetime.date(2016, 11, 23))

    def test_get_datetime(self):
        now = datetime.datetime.now()
        self.assertFunc(get_datetime, now.isoformat(), now)
        # add timezone info
        now = datetime.datetime.now(pytz.utc)
        self.assertFunc(get_datetime, now.isoformat(), now)
        self.assertFunc(get_datetime, "hello, world!", CoercianError)


if __name__ == '__main__':
    unittest.main()
