"""Markowik command line and programmatic interface."""

import argparse
import codecs
import re
import sys

import markdown

from markowik import util
from markowik.mdx import MarkowikExtension, BadURL, STRIPTAG

# =============================================================================
# programmatic interface
# =============================================================================

def convert(src, imagebaseurl="", htmlimages=False, encoding="UTF8", mx=None):
    """
    Convert Markdown to Google Code Wiki.

    Markdown source must be given as a string. Keyword arguments correspond to
    the similar named command line options.

    Raises a `BadURL` exception when links or images (including `imagebaseurl`)
    have URLs not supported (respectively recognized) by GCW.

    """
    # convert
    mx = mx or []
    mx.append(MarkowikExtension(imagebaseurl, htmlimages, encoding))
    md = markdown.Markdown(extensions=mx)
    wiki = md.convert(src)
    xpatt = r'^<%s>\n*|\n*</%s>$' % (STRIPTAG, STRIPTAG)
    wiki = re.sub(xpatt, '', wiki)

    # add pragmas
    meta = getattr(md, 'Meta', {})
    meta = dict((k.lower(), " ".join(v)) for k, v in meta.items())
    if any(x in meta for x in ('summary', 'labels')):
        summary = meta.get('summary', '')
        labels = meta.get('labels', '')
        wiki = "#summary %s\n#labels %s\n\n%s" % (summary, labels, wiki)

    # un-escape XML characters
    for x, y in [("&lt;", "<"), ("&gt;", ">"), ("&amp;", "&")]:
        wiki = wiki.replace(x, y)

    return wiki

# =============================================================================
# command line interface
# =============================================================================

def options():

    desc = """
        Convert Markdown to Google Code Wiki.
    """

    epilog = """
        Visit http://pypi.python.org/pypi/markowik for more detailed usage
        instructions.
    """

    p = argparse.ArgumentParser(description=desc, epilog=epilog)
    p.add_argument('input', metavar='INFILE',
                   help="markdown file")
    p.add_argument('output', metavar='OUTFILE', nargs='?', default=None,
                   help="wiki file (default: stdout)")
    p.add_argument('--mx', metavar='MX', nargs='*',
                   help="markdown extensions to activate")
    p.add_argument('--image-baseurl', metavar='URL', dest='imagebaseurl',
                   default="",
                   help="base URL to prepend to relative image locations")
    p.add_argument('--html-images', default=False, action='store_true',
                   dest='htmlimages',
                   help="always use HTML for images")
    p.add_argument('--encoding', default='UTF8',
                   help="encoding of input and output (default: %(default)s)")
    p.add_argument('--quiet', default=True, action='store_false',
                   dest='verbose',
                   help="disable info messages")

    return p.parse_args()

def abort(msg):

    print("abort: %s" % msg)
    sys.exit(1)

def main():

    opts = options()
    util.VERBOSE = opts.verbose
    try:
        with codecs.open(opts.input, 'r', opts.encoding) as fp:
            md = fp.read()
    except IOError as e:
        abort("failed to open input file (%s)" % e)

    kwds = ('imagebaseurl', 'htmlimages', 'encoding', 'mx')
    kwds = dict((k, getattr(opts, k)) for k in kwds)
    try:
        wiki = convert(md, **kwds)
    except BadURL as e:
        abort(e)

    if opts.output:
        try:
            with codecs.open(opts.output, 'w', opts.encoding) as fp:
                fp.write(wiki)
        except IOError as e:
            abort("failed to write output file (%s)" % e)
    else:
        print wiki.encode(opts.encoding)
