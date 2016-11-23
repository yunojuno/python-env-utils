.. image:: https://travis-ci.org/yunojuno/python-env-utils.svg?branch=master
    :target: https://travis-ci.org/yunojuno/python-env-utils

.. image:: https://badge.fury.io/py/env_utils.svg
    :target: https://badge.fury.io/py/env_utils

.. image:: https://codecov.io/gh/yunojuno/python-env-utils/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/yunojuno/python-env-utils

env utils
=========

This library extends the standard library's ``getenv`` function, allowing
you to coerce the return value into a type.

And that's it.

It's been released as a library because every project we have includes the
same requirements - read in environment variables, coerce them into the
correct type.

The problem is that environment variables are always stored as strings, but
Python will evaluate any string (even "") as True if cast to a boolean. This
is almost never the desired behaviour. If you set an environment variable to
"", "0" or "False", you want it to be False.

.. code:: python

    >>> os.environ['foo'] = "0"
    >>> val = os.getenv('foo')
    >>> val
    "0"
    >>> bool(val)
    True

``env_utils.get_env`` will coerce the value into the type you require. The package contains basic helper functions that coerce booleans, integers, decimals, floats, dates, lists and dictionaries.

.. code:: python

    # FOO=0
    >>> env_utils.get_env('FOO')
    "0"
    >>> env_utils.get_bool('FOO')
    False
    >>> env_utils.get_int('FOO')
    0

    # FOO=foo,bar
    >>> env_utils.get_list('FOO', separator=',')
    ['foo', 'bar']

    # FOO='{"foo": true}'
    >>> env_utils.get_dict('FOO')
    {'foo': True}

    # FOO=2016-11-23
    >>> env_utils.get_date('FOO')
    datetime.date(2016, 11, 23)

You can supply any function you like to coerce the value, e.g.:

.. code:: python

    >>> import os
    >>> os.getenv('FOO_NAME')
    'bob'
    >>> class Foo(object):
    ...     def __init__(self, name):
    ...         self.name = name
    >>> coerce = lambda x: Foo(x)
    >>> import env_utils
    >>> foo = env_utils.get_env('FOO_NAME', coerce=coerce)
    >>> foo.name
    >>> 'bob'


Installation
------------

The library is available at pypi as 'env_utils', and can installed using pip::

    $ pip install env_utils

Tests
-----

The tests can be run using ``tox``:

.. code:: shell

    $ tox
