"""Markowik Markdown extension."""

from itertools import izip_longest
import os
import re
import textwrap

import markdown.treeprocessors
from markdown.util import etree, STX

from markowik.util import dump, log, truncate, escapewikiwords

# =============================================================================

DEBUG = "MARKOWIK_DEBUG" in os.environ

SPANLEVELTAGS = """
em strong code
span sub sup
img a
""".strip().split() # need only those known to TagFormatter

STRIPTAG = 'we_need_this_to_preserve_leading_and_trailing_whitespace'

# GCW expects image URLs to match this:
RXIMGEXT = re.compile(r'\.(?:svg|png|gif|jpe?g)$', re.IGNORECASE)

# Absolute URLs
RXABSURL = re.compile(r'^(?:[a-z]+:)?//')

# In GCW, URLs must match this:
RXABSURLX = re.compile(r'^(?:https?|ftp)://')

# Valid GCW page names:
RXPAGENAME = re.compile(r'^\w+$')

# (mis)using control characters:
DDX = u'\u0004' # dedent marker for a line
TRX = u'\u0005' # temporary replacement marker

# =============================================================================

class BadURL(Exception):
    """
    Indicates an invalid or missing protocol in a URL.

    """
    def __init__(self, url):
        msg = ("the URL '%s' has an invalid or missing protocol prefix (must "
               "be one of http, https, or ftp)" % url)
        super(BadURL, self).__init__(msg)

# =============================================================================

class TagFormatter(object):

    def __init__(self, mdx):
        self.mdx = mdx
        self.liststack = []
        self.blockquotestack = []

    # -------------------------------------------------------------------------
    # state handling utilities
    # -------------------------------------------------------------------------

    def onenter(self, tag):
        if tag in ('ul', 'ol'):
            self.liststack.append(tag)
        elif tag == 'blockquote':
            self.blockquotestack.append(tag)

    def onleave(self, tag):
        if tag in ('ul', 'ol'):
            self.liststack.pop()
        elif tag == 'blockquote':
            self.blockquotestack.pop()

    # -------------------------------------------------------------------------
    # helpers
    # -------------------------------------------------------------------------

    def element(self, tag, text, attrib=None):
        """
        Get an XML element named `tag` with content `text` and attributes
        `attrib` as plain text. This is just a convenience function which makes
        life easier when attributes have to be considered.

        """
        # Note: we do not use `etree.Element()` and `etree.tostring()` because
        # they yield some character encoding issues, especially in attribute
        # values.
        elem = ["<%s" % tag]
        for k, v in (attrib or {}).items():
            try:
                v = v.replace('"', "''")
            except AttributeError: # not a string, ignore
                continue
            elem.append(' %s="%s"' % (k, v))
        elem += [">%s</%s>" % (text, tag)] if text else [" />"]
        return "".join(elem)

    def block(self, front, text, islist=False, isblockquote=False):
        """
        Format a converted block element (i.e. `text` is already in wiki
        syntax) in context of its preceding wiki code (given by `front`).

        """
        text = text.strip("\n")
        nestedblock = ((len(self.liststack) - islist) or
                       len(self.blockquotestack) - isblockquote)
        if nestedblock:
            noheadlb = any(front.endswith(x) for x in ("\n", "* ", "# "))
            head = "" if noheadlb else "\n"
            tail = "\n"
        else:
            head = ""
            tail = "\n\n"
        return "%s%s%s" % (head, text, tail)

    # -------------------------------------------------------------------------
    # tag content formatter
    # -------------------------------------------------------------------------

    idletags = ('div', 'thead', 'tbody')

    htmlspanleveltags = ('sub', 'sup')

    def __getattr__(self, name):

        if name in self.idletags:
            return lambda _, text, *x: text
        if name in self.htmlspanleveltags:
            return lambda _, text, *x: '<%s>%s</%s>' % (name, text, name)

        raise AttributeError(name)

    def strong(self, _front, text, _attrib):
        return "*%s*" % text

    def em(self, _front, text, _attrib):
        return "_%s_" % text

    def code(self, _front, text, _attrib):
        return ("{{{%s}}}" if "`" in text else "`%s`") % text

    def p(self, front, text, _attrib):
        return self.block(front, text)

    def pre(self, front, text, _attrib):
        text = ("\n%s" % DDX).join(text.split("\n"))
        return self.block(front, "{{{\n%s%s\n}}}" % (DDX, text))

    def h1(self, _front, text, _attrib):
        return "= %s =\n\n" % text

    def h2(self, _front, text, _attrib):
        return "== %s ==\n\n" % text

    def h3(self, _front, text, _attrib):
        return "=== %s ===\n\n" % text

    def h4(self, _front, text, _attrib):
        return "==== %s ====\n\n" % text

    def h5(self, _front, text, _attrib):
        return "===== %s =====\n\n" % text

    def h6(self, _front, text, _attrib):
        return "====== %s ======\n\n" % text

    def ul(self, front, text, _attrib):
        return self.block(front, text, islist=True)

    def ol(self, front, text, attrib):
        return self.ul(front, text, attrib)

    def li(self, _front, text, _attrib):
        c = "#" if self.liststack[-1] == 'ol' else "*"
        text = "\n  ".join(text.split("\n"))
        return "  %s %s\n" % (c, text.strip())

    def br(self, _front, _text, _attrib):
        return "<br/>\n"

    def hr(self, front, _text, _attrib):
        return self.block(front, "-" * 10)

    def blockquote(self, front, text, _attrib):
        text = "\n  ".join(text.split("\n"))
        return self.block(front, "  %s\n" % (text.strip()), isblockquote=True)

    def a(self, _front, text, attrib):
        if attrib['html']:
            log("using an HTML link for '%s'" % text)
            return self.element('a', text, attrib)
        return "[%s %s]" % (attrib['href'], text)

    def img(self, _front, _s, attrib):
        if self.mdx.htmlimages:
            return self.element('img', None, attrib)
        return attrib['src']

    def dl(self, front, text, _attrib):
        text = "<dl>\n%s</dl>" % text
        return self.block(front, text)

    def dt(self, _front, text, _attrib):
        return "<dt>%s</dt>\n" % text.strip("\n")

    def dd(self, _front, text, _attrib):
        return "<dd>%s</dd>\n" % text.strip("\n")

    def span(self, _front, text, attrib):
        return self.element('span', text, attrib)

    def table(self, front, text, _attrib):
        return self.block(front, text)

    def tr(self, _front, text, _attrib):
        return "%s||\n" % text

    def th(self, _front, text, _attrib):
        return "|| *%s* " % text

    def td(self, _front, text, _attrib):
        return "|| %s " % text

# =============================================================================

class MarkowikPreprocessor(markdown.preprocessors.Preprocessor):

    def run(self, lines):
        lines = "\n".join(lines)
        lines = tocomat(lines)
        return lines.split("\n")

class MarkowikTreeprocessor(markdown.treeprocessors.Treeprocessor):
    """
    Walks through an XHTML element tree and converts it to GCW syntax.

    """
    formatter = None

    def __init__(self, mdx):
        markdown.treeprocessors.Treeprocessor.__init__(self)
        self.mdx = mdx

    def run(self, root):
        """
        Walk and edit the tree given by `root`.

        """

        dump(root, "XHTML")

        self.preprocess(root, None)

        dump(root, "Preprocessed")

        wiki = self.convert("", root, TagFormatter(self.mdx))

        # dedent according to DDX markers:
        wiki = re.sub(r'\n *%s' % DDX, '\n', wiki)

        elem = etree.Element(STRIPTAG)
        elem.text = wiki
        root.clear()
        root.append(elem)

        dump(root, "Flattened")

        dump(None, "Wiki")

        return root

    def preprocess(self, node, nextnode):
        """
        Preprocess the XHTML tree generated by `markdown.convert()`.

        """
        # --- inject linebreaks between subsequent nested paragraphs ----------

        if node.tag in ('li', 'blockquote'):
            prev = None
            index = 0
            minindex = 1 if node.tag == 'li' else 0
            lb = etree.Element('br')
            for child in list(node):
                # For whatever reason, the first linebreak in a list item
                # introduces a new paragraph in GCW while subsequent linebreaks
                # are handled as whitespace, i.e. in these cases an explicit
                # <br/> is needed.
                if index > minindex and prev.tag == 'p' and child.tag == 'p':
                    log("using <br/> to fake nested paragraph '%s'" %
                        truncate(child.text or "...", 15))
                    node.insert(index, lb)
                    index += 1
                index += 1
                prev = child

        # --- replace <abbr> by <span> ----------------------------------------

        if node.tag == 'abbr':
            log("replacing <abbr> by <span> ('%s')" % truncate(node.text, 15))
            node.tag = 'span'

        # --- collapse <pre><code> to <pre> -----------------------------------

        precodeblock = (node.tag == 'pre' and len(node) == 1 and not node.text
                        and node[0].tag == 'code' and not node[0].tail)
        if precodeblock:
            child = node[0]
            node.clear()
            node.text = child.text

        # --- whitespace cleanup ----------------------------------------------

        node.text = node.text or ""
        node.tail = node.tail or ""
        if not (node and node[0].tag in SPANLEVELTAGS):
            node.text = node.text.strip("\n")
        if (not (node.tag in SPANLEVELTAGS and node.tail) and
            not (nextnode and nextnode.tag in SPANLEVELTAGS)):
            node.tail = node.tail.strip("\n")
        if node.tag != 'pre':
            node.text = re.sub(r'\s+', ' ', node.text or "")
        else:
            node.text = textwrap.dedent(node.text)
            assert not node
        node.tail = re.sub(r'\s+', ' ', node.tail or "")

        # --- prefix image urls -----------------------------------------------

        if node.tag == 'img':
            isrc = node.attrib['src']
            if not RXABSURL.search(isrc):
                isrc = "%s%s" % (self.mdx.imagebaseurl, isrc)
            if not RXABSURLX.search(isrc):
                raise BadURL(isrc)
            if not RXIMGEXT.search(isrc):
                conn = "&" if "?" in isrc else "?"
                isrc = "%s%sx=x.png" % (isrc, conn)
                log("appending artificial image file extension (%s)" % isrc)
            node.attrib['src'] = isrc

        # --- check link URLs -------------------------------------------------

        if node.tag == 'a':
            url = node.attrib['href']
            if RXABSURL.search(url):
                if not RXABSURLX.search(url):
                    raise BadURL(url)
            elif not RXPAGENAME.search(url):
                raise BadURL(url)

        # --- traverse child nodes --------------------------------------------

        for child, nextnode in izip_longest(node, node[1:]):
            self.preprocess(child, nextnode)

    def convert(self, front, node, formatter):
        """
        Convert the elements tree `node` to wiki syntax.

        The preceding wiki context is given in `front`, the wiki text converted
        so far.

        """
        def escaped(node, x):
            """Escape GCW reserved characters and WikiWords."""

            if node.tag in ('pre', 'code'):
                return x
            if node.tag != 'a':
                x = escapewikiwords(x)
            if node.tag == 'a' and not node.attrib['html']:
                return x
            x = re.sub(r'`', TRX, x)
            x = re.sub(r'({{{|}}})', r'`\1`', x)
            x = re.sub(TRX, '{{{`}}}', x)
            x = re.sub(r'([[\]_*])', r'`\1`', x)
            return x

        # --- links need special handling -------------------------------------

        if node.tag == 'a':
            plainimagelink = (len(node) == 1 and node[0].tag == 'img'
                              and not node.text and not node[0].tail)
            if plainimagelink and not self.mdx.htmlimages:
                isrc = node[0].attrib['src']
                href = node.attrib['href']
                node.clear()
                node.attrib['href'] = href
                node.text = isrc
                node.tail = ""
                html = False
            else:
                text = node.text or ""
                html = bool(node) or "]" in text or STX in text
            node.attrib['html'] = html

        # --- recursively convert node contents, leaves first -----------------

        s = escaped(node, node.text)
        for child in node:
            formatter.onenter(child.tag)
            s += self.convert(front + s, child, formatter)
            s += escaped(node, child.tail)
            formatter.onleave(child.tag)

        return getattr(formatter, node.tag)(front, s, node.attrib)

# =============================================================================

class MarkowikExtension(markdown.Extension):
    """The markdown extension that saves your life."""

    def __init__(self, imagebaseurl, htmlimages, encoding):
        markdown.Extension.__init__(self)
        self.imagebaseurl = imagebaseurl
        self.htmlimages = htmlimages
        self.encoding = encoding

    def extendMarkdown(self, md, md_globals):

        pp = MarkowikPreprocessor()
        tp = MarkowikTreeprocessor(self)
        md.preprocessors.add('markowik', pp, '_end')
        md.treeprocessors.add('markowik', tp, '_end')

# =============================================================================

def tocomat(md):
    r"""
    Replace a `[TOC X]` marker by a GCW TOC-tag with depths X.

    The marker must be separated with empty lines from surrounding text. A
    default depths of 1 is used when X is no given.

    Examples:

    >>> tocomat('[TOC]')
    '<wiki:toc max_depth="1" />'

    >>> tocomat('[TOC 3]')
    '<wiki:toc max_depth="3" />'

    >>> tocomat('[TOC 3]\n...')
    '[TOC 3]\n...'

    >>> tocomat('...\n[TOC 3]')
    '...\n[TOC 3]'

    >>> tocomat('...\n\n[TOC6]')
    '...\n\n<wiki:toc max_depth="6" />'

    """
    def repl(match):
        head, level, tail = match.groups()
        level = level or "1"
        return '%s<wiki:toc max_depth="%s" />%s' % (head, level, tail)

    return re.sub(r'(^\n*|\n\n)\[TOC *([1-6]|)\](\n\n|\n*$)', repl, md)
