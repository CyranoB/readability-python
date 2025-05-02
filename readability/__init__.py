"""Python Readability - Extract the main content from web pages.

A Python port of the go-readability library.
"""

__version__ = "0.5.0"

from readability.parser import Readability
from readability.models import Article

__all__ = ["Readability", "Article"]
