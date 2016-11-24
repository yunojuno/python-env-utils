# -*- coding: utf-8 -*-
import datetime
from decimal import Decimal, InvalidOperation
import inspect
import pytz
import unittest
from test.test_support import EnvironmentVarGuard

from env_utils import (
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
    coerce_bool,
    coerce_int,
    coerce_float,
    coerce_decimal,
    coerce_dict,
    coerce_datetime,
    coerce_date,
)


class TestFunctions(unittest.TestCase):

    """Basic function tests."""

    def assertFunc(self, func, value, expected):
        self.environ["foo"] = value
        if inspect.isclass(expected):
            self.assertRaises(expected, func, 'foo')
        else:
            self.assertEqual(func("foo"), expected)

    def setUp(self):
        self.environ = EnvironmentVarGuard()

    def test_coerce_bool(self):
        self.assertEqual(coerce_bool("true"), True)
        self.assertEqual(coerce_bool("TRUE"), True)
        self.assertEqual(coerce_bool("1"), True)
        self.assertEqual(coerce_bool("y"), True)
        self.assertEqual(coerce_bool("tru"), False)
        self.assertEqual(coerce_bool("0"), False)
        self.assertEqual(coerce_bool(None), False)

    def test_coerce_int(self):
        self.assertEqual(coerce_int("01"), 1)
        self.assertRaises(ValueError, coerce_int, "foo")

    def test_coerce_float(self):
        self.assertEqual(coerce_float("01"), 1.0)
        self.assertRaises(ValueError, coerce_float, "foo")

    def test_coerce_decimal(self):
        self.assertEqual(coerce_decimal("01"), Decimal('1.0'))
        self.assertRaises(InvalidOperation, coerce_decimal, "foo")

    def test_coerce_dict(self):
        self.assertEqual(coerce_dict("false"), False)
        self.assertEqual(coerce_dict("{\"foo\": false}"), {'foo': False})
        self.assertRaises(ValueError, coerce_dict, "hello, world!")

    def test_coerce_datetime(self):
        now = datetime.datetime.now()
        self.assertEqual(coerce_datetime(now.isoformat()), now)
        # add timezone info
        now = datetime.datetime.now(pytz.utc)
        self.assertEqual(coerce_datetime(now.isoformat()), now)
        self.assertRaises(ValueError, coerce_datetime, "hello, world!")

    def test_coerce_date(self):
        today = datetime.date.today()
        self.assertEqual(coerce_date(today.isoformat()), today)
        # add timezone info
        self.assertRaises(ValueError, coerce_date, "hello, world!")

    def test__get_env(self):
        # env var is missing
        func = lambda x: x
        self.assertRaises(RequiredSettingMissing, _get_env, "bar", None, func, True)
        self.assertEqual(_get_env("bar", 'baz'), 'baz')
        # env var exists
        self.environ['FOO'] = 'bar'
        self.assertEqual(_get_env('FOO', None), 'bar')
        # env var coercian fails
        func = lambda x: int(x)
        self.assertRaises(Exception, _get_env, "FOO", coerce=func)

    def test_get_env(self):
        # too many args - we only support one default value ('bar')
        self.assertRaises(AssertionError, get_env, 'foo', 'bar', 'baz')
        # missing env var, use default
        del self.environ['FOO']
        self.assertRaises(RequiredSettingMissing, get_env, 'FOO', coerce=lambda x: x)
        self.assertEqual(get_env('FOO', 'bar', coerce=lambda x: x), 'bar')
        # valid env var
        self.assertFunc(get_env, 'foo', 'foo')

    def test_get_bool(self):
        self.assertFunc(get_bool, "bar", False)
        self.assertFunc(get_bool, "1", True)

    def test_get_int(self):
        self.assertFunc(get_int, "1", 1)
        self.assertFunc(get_int, "bar", Exception)

    def test_get_float(self):
        self.assertFunc(get_float, "1.0", 1.0)
        self.assertFunc(get_float, "bar", Exception)

    def test_get_decimal(self):
        self.assertFunc(get_decimal, "1", Decimal("1"))
        self.assertFunc(get_decimal, "bar", Exception)

    def test_get_list(self):
        self.assertFunc(get_list, "false", ['false'])
        self.assertFunc(get_list, "true false", ['true', 'false'])
        self.environ['foo'] = "true,false"
        self.assertEqual(get_list('foo', separator=','), ['true', 'false'])
        self.assertEqual(get_list('foo', ["baz"]), ['true,false'])

    def test_get_dict(self):
        self.assertFunc(get_dict, "false", False)
        self.assertFunc(get_dict, "{\"foo\": false}", {'foo': False})
        self.assertFunc(get_dict, "hello, world!", ValueError)

    def test_get_date(self):
        self.assertFunc(get_date, "2016-11-23", datetime.date(2016, 11, 23))
        self.assertFunc(get_date, "hello, world!", ValueError)

        # get_date also supports other date formats
        self.environ["foo"] = "23-11-2016"
        self.assertEqual(get_date("foo"), datetime.date(2016, 11, 23))

    def test_get_datetime(self):
        now = datetime.datetime.now()
        self.assertFunc(get_datetime, now.isoformat(), now)
        # add timezone info
        now = datetime.datetime.now(pytz.utc)
        self.assertFunc(get_datetime, now.isoformat(), now)
        self.assertFunc(get_datetime, "hello, world!", ValueError)


if __name__ == '__main__':
    unittest.main()
