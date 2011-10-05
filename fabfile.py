import codecs
import glob
import os
import re

from fabric.api import local, abort, lcd

import tests

HERE = os.path.dirname(__file__)
ROOT = HERE

# =============================================================================
# internal helpers
# =============================================================================

def _readfile(fname):
    """Shortcut for reading a text file."""

    with open(fname) as fp:
        content = fp.read()
    return content

def _contains(fname, rx, reflags=0):
    """Check if content of `fname` matches (contains) `rx`."""

    content = _readfile(fname)
    return re.search(rx, content, reflags)

def _needcleanworkingcopy():
    """Aborts if working copy is dirty."""

    if local("hg status -n", capture=True):
        abort("dirty working copy")

# =============================================================================
# wiki tools
# =============================================================================

WIKI = os.path.join(ROOT, "wiki") # clone in sub-directory `wiki`

WIKITESTPAGE = """
#summary Generated test illustration page
#labels Test, Generated

*Note*: The Markdown and wiki source shown here might not be displayed
perfectly. Especially code block markers `{{{` and `}}}` are always flushed
left completely. If in doubt, look at the source of this Wiki page or check the
original test files.

Converter command used for this test:

{{{
$ markowik MDFILE WIKIFILE %(options)s
}}}

Markowik revision: r%(revision)s

= <font color="darkred">Markdown Source</font> =

{{{
%(md)s
}}}

= <font color="darkred">Wiki Source</font> =

{{{
%(wiki)s
}}}

= <font color="darkred">Wiki View</font> =

%(wiki)s
""".strip()

def wiki_render():
    """Render wiki test pages."""

    _needcleanworkingcopy()

    context = {'revision': local("hg id -i", capture=True)}

    for testpage in glob.glob(os.path.join(WIKI, "Test*.wiki")):
        os.remove(testpage)

    for name, mdfile, wikifile, cfgfile in tests.iterfiles("md", "wiki", "cfg"):

        name = "".join(x.capitalize() for x in name.split("-"))
        pagefile = os.path.join(WIKI, "Test%s.wiki" % name)

        context['options'] = " ".join(tests.readoptions(cfgfile))

        with codecs.open(mdfile, 'r', 'UTF8') as fp:
            context['md'] = fp.read().strip("\n")
        with codecs.open(wikifile, 'r', 'UTF8') as fp:
            context['wiki'] = fp.read().strip("\n")
        with codecs.open(pagefile, 'w', 'UTF8') as fp:
            fp.write(WIKITESTPAGE % context)

def wiki_publish():
    """Publish wiki test pages."""

    dirty = lambda: local('hg status -n -I "Test*.wiki"', capture=True)

    with lcd(WIKI):
        if dirty():
            local('hg commit -A -m "Automatic update of test pages" -I "Test*.wiki"')
        local("hg fetch")
        local("hg push -r .")

def wiki():
    """Render and publish wiki test pages."""

    wiki_render()
    wiki_publish()

# =============================================================================
# release tools
# =============================================================================

def push():
    """Push master branch."""

    _needcleanworkingcopy()

    hgignore = _readfile(".hgignore").split("\n")[2:]
    gitignore = _readfile(".gitignore").split("\n")
    if hgignore != gitignore:
        abort("hg and git ignore files differ")

    local("hg push -r master google")
    local("hg push -r master bitbucket")
    local("hg push -r master github")

def release_check(version):
    """Various checks to be done prior a release."""

    # --- check README --------------------------------------------------------

    from docutils.core import publish_cmdline
    readme = os.path.join(ROOT, "README.rst")
    publish_cmdline(argv=["--halt", "2", readme, os.devnull])

    # --- version numbers -----------------------------------------------------

    rx = r'\n==+\nChanges\n==+\n\n--+\nVersion %s\n--+\n\n' % version
    if not _contains(readme, rx):
        abort("bad version in README.rst")

    setup = os.path.join(ROOT, "setup.py")
    rx = r'''\nversion *= *['"]%s['"]\n''' % version
    if not _contains(setup, rx):
        abort("bad version in setup.py")

    # --- run tests -----------------------------------------------------------

    local(os.path.join(ROOT, "bin", "tests"))

    # --- check working copy --------------------------------------------

    _needcleanworkingcopy()

    out = local("hg bookmarks", capture=True)
    if not re.match(r'\s*\* master\s', out):
        abort("working copy is not at master bookmark")

def release(version):
    """Make a release."""

    local("bin/buildout")

    release_check(version)

    local("rm -r %s" % os.path.join(ROOT, "build"))
    local("rm -r %s" % os.path.join(ROOT, "dist"))

    local("bin/buildout setup %s clean build sdist" % ROOT) # test build

    local("hg tag %s" % version)

    local("bin/buildout setup %s register sdist upload" % ROOT)

    push()
