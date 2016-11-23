env_utils
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

``env_utils.get_env`` will coerce the value into the type you require. It can
coerce booleans, integers, decimals, floats, dates, lists and dictionaries.

.. code:: python

    >>> env_utils.get_env('foo')
    "0"
    >>> env_utils.get_bool('foo')
    False
    >>> env_utils.get_int('01')
    1
    >>> env_utils.get_list('foo bar')
    ['foo', 'bar']
    >>> env_utils.get_dict('{"foo": true}")
    {'foo': True}
    >>> env_utils.get_date('2016-11-23')
    datetime.date(2016, 11, 23)
    >>> env_utils.get_float('1')
    1.0


Installation
------------

The library is available at pypi as 'env_utils', and can installed using pip::

    $ pip install env_utils

Tests
-----

There are tests in the package - they can be run using ``unittest``::

    $ python -m unittest env_utils.tests
