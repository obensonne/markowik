"""Miscellaneous utilities."""

import os
import re
import sys

from markdown.util import etree, STX, ETX

# -----------------------------------------------------------------------------

_rxwikiword = re.compile(r'(?<![a-z0-9])'
                          '((?:[A-Z][a-z0-9][a-z0-9_]*){2,})'
                          '(?![A-Za-z0-9"])')

def escapewikiwords(text):
    """
    Escape WikiWords with a prefixed `!`.

    >>> from textwrap import fill

    >>> wikiwords = (
    ...     "FooBar", "FooBarBaz", "Foo2Bar", "FooB2ar", "FooBar-2.0",
    ...     "Foo1234BarBong", "Foo1234Bong", "FooB20-1", "FooX99", "FooX11b-2",
    ...     "FooB00_0XY", "FoBaX2", "FooBar_FooBar"
    ... )

    >>> print fill(" ".join(escapewikiwords(x) for x in wikiwords))
    !FooBar !FooBarBaz !Foo2Bar !FooB2ar !FooBar-2.0 !Foo1234BarBong
    !Foo1234Bong !FooB20-1 !FooX99 !FooX11b-2 !FooB00_0XY !FoBaX2
    !FooBar_FooBar

    >>> normalwords = (
    ...     "Foobar", "Foo", "F", "FooB2XY", "FooBAR", "FooBaRR", "Foo1234x-0",
    ...     "Foo2000", "Foo2000x", "FooBA00", "FooBarX", "xFooBar",
    ...     "FooBarx2Z",
    ... )

    >>> print fill(" ".join(escapewikiwords(x) for x in normalwords))
    Foobar Foo F FooB2XY FooBAR FooBaRR Foo1234x-0 Foo2000 Foo2000x
    FooBA00 FooBarX xFooBar FooBarx2Z

    """
    return _rxwikiword.sub(r'!\1', text)

# -----------------------------------------------------------------------------

DEBUG = "MARKOWIK_DEBUG" in os.environ

def dump(obj, title=None):
    """
    Dump an object to stdout (when debug mode is on).

    The dump is preceded by a rule which may contain a `title`.

    """
    if not DEBUG:
        return
    title = (" %s " % title) if title else ""
    print(title.center(79, "-"))
    if obj is None:
        return
    if etree.iselement(obj):
        etree.dump(obj)
    else:
        print obj

# -----------------------------------------------------------------------------

VERBOSE = False

def log(msg):
    """
    Log `msg` to stderr (if verbose mode is on).

    PyMD-special string fractions are sanitized before logging.

    """
    if not VERBOSE:
        return
    msg = re.sub('%s.*?%s' % (STX, ETX), '<..>..<..>', msg)
    sys.stderr.write("info: %s\n" % msg)

# -----------------------------------------------------------------------------

def truncate(text, width=15):
    """Truncate some text end append an ellipsis.

    Linebreaks are replaced by whitespace.

    >>> truncate("1234567890", 10)
    '1234567890'
    >>> truncate("1234567890", 9)
    '123456...'
    >>> truncate("1234567890", 8)
    '12345...'
    >>> truncate("12\\n34", 10)
    '12 34'

    """
    text = text.replace("\n", " ")
    return "%s..." % text[:width-3] if len(text) > width else text
