===============================================================================
Markowik
===============================================================================

Markowik converts `Markdown`_ to `Google Code Wiki`_.

.. _`Google Code Wiki`: http://code.google.com/p/support/wiki/WikiSyntax
.. _`Markdown`: http://daringfireball.net/projects/markdown/

|flattr|

Markowik is able to convert most Markdown constructs to its Google Code Wiki
(GCW) equivalents. Instead of listing all supported conversions here, please
have a look at Markowik's `test suite show case`__.

.. __: http://code.google.com/p/markowik/w/list?q=label:Test

.. contents::
   :depth: 1
   :local:

-------------------------------------------------------------------------------
Installation
-------------------------------------------------------------------------------

Markowik requires Python 2.6 or 2.7.

Run::

    pip install markowik

or::

    easy_install markowik

You can also use Markowik without installation, as described under
`Contributions`_.

-------------------------------------------------------------------------------
Usage
-------------------------------------------------------------------------------

Command Line
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

From the help output::

    usage: markowik [-h] [--mx [MX [MX ...]]] [--image-baseurl URL]
                    [--html-images] [--encoding ENCODING] [--quiet]
                    INFILE [OUTFILE]

    Convert Markdown to Google Code Wiki.

    positional arguments:
      INFILE               markdown file
      OUTFILE              wiki file (default: stdout)

    optional arguments:
      -h, --help           show this help message and exit
      --mx [MX [MX ...]]   markdown extensions to activate
      --image-baseurl URL  base URL to prepend to relative image locations
      --html-images        always use HTML for images
      --encoding ENCODING  encoding of input and output (default: UTF8)
      --quiet              disable info messages

Markdown extensions may be given similarly as to the `Python Markdown`_ (PyMD)
command line tool, with the exception that individual extensions must be
separated by a space::

    $ markowik INPUT --mx tables def_list

The currently supported (i.e. tested) extensions are *abbr*, *tables*, and
*def_list*. Other extensions generally should work too but might yield
unexpected results in the converted wiki text.

Concerning the option ``--html-images``, see the explanations below at
`Caveats`_.

.. _`Python Markdown`: http://www.freewisdom.org/projects/python-markdown/
.. _`PyMD`: http://www.freewisdom.org/projects/python-markdown/

Programmatic
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Markowik is implemented in Python. The *markowik* module provides a function
named ``convert``. Semantically it is similar to the command line interface
(keyword arguments correspond to command line options). Here's a short usage
example::

    >>> import markowik
    >>> markowik.convert("Some *markdown* text ...", mx=['tables'])
    u'Some _markdown_ text ...'

Page Pragmas
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

GCW `page pragmas`_ can be set in Markdown source files as meta data in the
format defined by the PyMD `meta extension`_::

    >>> src = """Summary: page summary
    ... Labels: some, labels
    ...
    ... Here starts the *page* ..
    ... """
    >>> print markowik.convert(src, mx=['meta'])
    #summary page summary
    #labels some, labels
    <BLANKLINE>
    Here starts the _page_ ..

Note that the meta extension has to be enabled explicitly, i.e. by default
Markowik does not recognize page pragmas.

.. _`page pragmas`: http://code.google.com/p/support/wiki/WikiSyntax#Pragmas
.. _`meta extension`: http://www.freewisdom.org/projects/python-markdown/Meta-Data

Caveats
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

GCW cannot express all markup possible in Markdown. This means Markdown source
files should be written with the following limitations in mind.

URLs in Links and Images
''''''''''''''''''''''''

URLs used for links or image sources have to be absolute and must have a
specific protocol to get recognized by GCW. In particular, any URL must start
with ``http://``, ``https://``, or ``ftp://``. Markowik *aborts the conversion*
if it finds URLs not matching these requirements.

Typefacing in Link Names
''''''''''''''''''''''''

GCW does not support typefacing in link names. For instance GCW renders the
link name in ``[http://foo.com _Foo_]`` literally, i.e. as ``_Foo_``. However,
GCW recognizes typefacing in HTML links, i.e. ``<a
href="http://foo.com">_Foo_</a>`` is emphasized properly. For this reason
Markdown links with nested typefacing like ``[*Foo*](http://foo.com)`` will be
converted to HTML links. As a result, link labels with certain special
characters which have to be escaped in GCW using backtick (`````) markers will
also result in HTML links.

Nested Paragraphs
'''''''''''''''''

GCW does not really support multiple nested paragraphs (e.g. in lists or
blockquotes). Markowik simulates multiple nested paragraphs by separating them
with a ``<br/>`` (which visually mimics paragraphs but does not break the
nesting environment).

Images
''''''

Markdown allows to express alternative and title texts for images. GCW's image
syntax does not support this. The only way to preserve these texts is to use
plain HTML ``<img>`` tags. The option ``--html-images`` enables this
workaround.

Another issue is that GCW expects image URLs to end with an image file type
extension. Markowik adds artificial image extensions if necessary, for instance
``http://foo.bar/image`` is changed to ``http://foo.bar/image?x=x.png``.

Abbreviations
'''''''''''''

GCW has no markup for `abbreviations`__ nor does it support the HTML tag
``<abbr>``. Markowik converts abbreviations to ``<span>``-elements which kind
of mimics abbreviations (in a limited fashion of course).

.. __: http://www.freewisdom.org/projects/python-markdown/Abbreviations

HTML
''''

Any plain HTML occurring in a Markdown source ends up literally in GCW  (with
the exception of the content of span-level tags). This means the Markdown
source should only contain `HTML supported by GCW`__. Another implication is
that URLs used in plain HTML tags are not checked for GCW compatibility. In
other words: when using raw HTML you are on your own!

.. __: http://code.google.com/p/support/wiki/WikiSyntax#HTML_support

-------------------------------------------------------------------------------
Resources
-------------------------------------------------------------------------------

:Releases and documentation: `PyPI`_

:Issues, source code, and test suite show case: `Google Code`_

:Source code mirrors: `BitBucket`_ and `GitHub`_

.. _`PyPI`: http://pypi.python.org/pypi/markowik
.. _`Google Code`: http://code.google.com/p/markowik
.. _`BitBucket`: https://bitbucket.org/obensonne/markowik
.. _`GitHub`: https://github.com/obensonne/markowik

-------------------------------------------------------------------------------
Contributions
-------------------------------------------------------------------------------

To contribute to Markowik, fork the project at `Google Code`_, `BitBucket`_,
or `GitHub`_.

Every fix or new feature should include one or more corresponding test cases
(check the `existing tests`_ for how tests should look like). Please also `post
an issue`_ describing your fix or enhancement.

.. _`existing tests`: http://code.google.com/p/markowik/source/browse#hg%2Fsrc%2Ftests
.. _`post an issue`: http://code.google.com/p/markowik/issues

Markowik uses  `Buildout`_ to easily set up the development environment.
Buildout automates the process of downloading and installing requirements to
use and develop Markowik. Requirements are installed local to the project
source directory, i.e. it does not clutter the system Python installation.

In a fresh source checkout, run::

    $ python bootstrap.py
    $ bin/buildout

When done, the following scripts can be found in the ``bin/`` directory:

``markowik``
    The Markowik command line tool, ready to use.

``tests``
    Test runner script (a wrapper for `nose`_).

``fab``
    `Fabric`_ binary to use for the project's *fabfile*.

``python``
    A Python interpreter whith acces to the local development version of
    the *markowik* module.

.. _`Buildout`: http://www.buildout.org/
.. _`nose`: http://readthedocs.org/docs/nose/
.. _`Fabric`: http://fabfile.org/

-------------------------------------------------------------------------------
Changes
-------------------------------------------------------------------------------

Version 0.2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Markowik now supports (and requires) `PyMD`_ ≥ 2.1. Next to minor API changes
  PyMD 2.1 also had some changes and improvements in its conversion process
  -- for details, `check how tests have been adjusted`__ for PyMD 2.1.

.. __: http://code.google.com/p/markowik/source/list?r=0.2

Version 0.1.2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Explicitly require `PyMD`_ 2.0.3 (this is a temporary fix until
  *markowik* correctly works with PyMD 2.1). **Note:** If this
  conflicts with requirements of other Python packages, run *markowik* in its
  own buildout as described above.
- Minor documentation tweaks.

Version 0.1.1
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Improved documentation.
- Minor fixes.

Version 0.1
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Initial release.

.. ......................................................................... ..

.. |flattr| image:: http://api.flattr.com/button/flattr-badge-large.png
   :alt: Flattr this
   :target: http://flattr.com/thing/410528/Markowik
