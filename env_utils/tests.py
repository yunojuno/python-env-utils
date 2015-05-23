# -*- coding: utf-8 -*-
"""env_utils tests."""

import os
import unittest

from . import getenv, int_, bool_


class TestFunctions(unittest.TestCase):

    """Basic function tests."""

    def test_getenv(self):
        """Test env_utils.getenv function."""
        self.assertEqual(getenv("foo"), None)
        self.assertEqual(getenv("foo", "bar"), "bar")
        os.environ['foo'] = "0"
        self.assertEqual(getenv("foo", coerce=bool_), False)
        os.environ['foo'] = "1"
        self.assertEqual(getenv("foo", coerce=int_), 1)
        os.environ['foo'] = "1"
        self.assertEqual(getenv("foo", coerce=lambda x: x+"."), "1.")

    def test_getenv_int(self):
        """Test env_utils.getenv function with integers."""
        os.environ["baz"] = "01"
        self.assertEqual(getenv("baz"), "01")
        self.assertEqual(getenv("baz", coerce=int_), 1)

    def test_int_(self):
        """Test int_ function."""
        self.assertEqual(int_("0"), 0)
        self.assertEqual(int_("01"), 1)
        self.assertRaises(AssertionError, int_, True)
        self.assertRaises(AssertionError, int_, None)
        self.assertRaises(ValueError, int_, "foo")
        self.assertRaises(ValueError, int_, "")

    def test_bool_(self):
        """Test bool_ function."""
        self.assertEqual(bool_(""), False)
        self.assertEqual(bool_("false"), False)
        self.assertEqual(bool_("True"), True)
        self.assertEqual(bool_("true"), True)
        self.assertEqual(bool_("1"), True)
        self.assertRaises(AssertionError, bool_, True)
        self.assertRaises(AssertionError, bool_, None)


if __name__ == '__main__':
    unittest.main()
