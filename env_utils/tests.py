# -*- coding: utf-8 -*-
"""env_utils tests."""
import os
import unittest

from env_utils import getenv, to_int, to_bool, get_bool


class TestFunctions(unittest.TestCase):

    """Basic function tests."""

    def test_getenv(self):
        """Test env_utils.getenv function."""
        self.assertEqual(getenv("foo"), None)
        self.assertEqual(getenv("foo", "bar"), "bar")
        os.environ['foo'] = "0"
        self.assertEqual(getenv("foo", coerce=to_bool), False)
        os.environ['foo'] = "1"
        self.assertEqual(getenv("foo", coerce=to_int), 1)
        os.environ['foo'] = "1"
        self.assertEqual(getenv("foo", coerce=lambda x: x+"."), "1.")

    def test_getenv_int(self):
        """Test env_utils.getenv function with integers."""
        os.environ["baz"] = "01"
        self.assertEqual(getenv("baz"), "01")
        self.assertEqual(getenv("baz", coerce=to_int), 1)

    def test_to_int(self):
        """Test to_int function."""
        self.assertEqual(to_int("0"), 0)
        self.assertEqual(to_int("01"), 1)
        self.assertRaises(AssertionError, to_int, True)
        self.assertRaises(AssertionError, to_int, None)
        self.assertRaises(ValueError, to_int, "foo")
        self.assertRaises(ValueError, to_int, "")

    def test_to_bool(self):
        """Test to_bool function."""
        self.assertEqual(to_bool(""), False)
        self.assertEqual(to_bool(""), False)
        self.assertEqual(to_bool("false"), False)
        self.assertEqual(to_bool("True"), True)
        self.assertEqual(to_bool("true"), True)
        self.assertEqual(to_bool("1"), True)
        self.assertEqual(to_bool(None), False)
        self.assertEqual(to_bool(True), True)
        self.assertEqual(to_bool(False), False)

    def test_get_bool(self):
        """Test get_bool function."""
        # baz is unset
        self.assertEqual(get_bool("baz", False), False)
        self.assertEqual(get_bool("baz", True), True)
        os.environ["baz"] = "True"
        self.assertEqual(get_bool("baz", False), True)
        self.assertRaises(AssertionError, get_bool, "baz", 0)


if __name__ == '__main__':
    unittest.main()
