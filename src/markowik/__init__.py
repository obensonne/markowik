"""Markowik converts Markdown to Google Code Wiki.

Detailed documentation can be found at http://pypi.python.org/pypi/markowik.

"""
import re

import markdown

from markowik.main import convert, BadURL

__all__ = ["convert", "BadURL"]
