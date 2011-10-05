import codecs
import difflib
import glob
import os
import subprocess
import sys

HERE = os.path.dirname(__file__)
MARKOWIK = os.path.join(HERE, "..", "..", "bin", "markowik")

def readoptions(fname):
    """
    Read `markowik` options from a file, one per line.

    """
    if os.path.exists(fname):
        with codecs.open(fname, 'r', 'UTF8') as fp:
            cfg = fp.read()
        options = [x.strip() for x in cfg.split("\n") if x.strip()]
    else:
        options = []

    return options

def iterfiles(*exts):
    """
    Iterate all test files.

    For each test file, a list is given whose first item is the test name and
    all subsequent items are test file paths, one for each file extension given
    in `exts`.

    """
    inputs = glob.glob(os.path.join(HERE, "*.md"))
    for fname in inputs:
        name = os.path.splitext(os.path.basename(fname))[0]
        yield [name] + [os.path.join(HERE, "%s.%s" % (name, x)) for x in exts]

def _test(testdata):
    """
    Test a specific test file (`testdata` is a list of related filenames).

    """
    mdfile, wikifile, outfile, cfgfile = testdata

    # --- options ---------------------------------------------------------

    options = readoptions(cfgfile)

    # --- run converter ---------------------------------------------------

    ret = subprocess.call([MARKOWIK, "--quiet", mdfile, outfile] + options)
    assert ret == os.EX_OK

    # --- load expected and actual results --------------------------------

    with codecs.open(wikifile, 'r', 'UTF8') as fp:
        wiki = fp.read().strip("\n") + "\n"
    with codecs.open(outfile, 'r', 'UTF8') as fp:
        out = fp.read().strip("\n") + "\n"

    os.remove(outfile)

    # --- compare results -------------------------------------------------

    if wiki != out:
        alines, blines = wiki.splitlines(True), out.splitlines(True)
        delta = difflib.unified_diff(alines, blines, fromfile=wikifile,
                                     tofile=outfile)
        for line in delta:
            sys.stdout.write(line)
        assert False

def test():
    """
    Test all test files

    This is a *nose* test generator function.

    """
    for x in iterfiles("md", "wiki", "out", "cfg"):

        _test.description = x[0]
        yield _test, x[1:]
