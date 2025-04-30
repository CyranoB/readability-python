"""Data models for Python Readability."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from bs4 import Tag


@dataclass
class Article:
    """Article represents the final readable content extracted from a web page.

    This class mirrors the Article struct from the Go implementation.
    """

    url: Optional[str] = None
    title: Optional[str] = None
    byline: Optional[str] = None
    node: Optional[Tag] = None  # BeautifulSoup Tag object
    content: Optional[str] = None  # HTML string
    text_content: Optional[str] = None  # Plain text
    length: int = 0  # Character count
    excerpt: Optional[str] = None
    site_name: Optional[str] = None
    image: Optional[str] = None
    favicon: Optional[str] = None
    language: Optional[str] = None
    published_time: Optional[datetime] = None
    modified_time: Optional[datetime] = None


class ParsingError(Exception):
    """Base exception for parsing errors."""
    pass


class ExtractionError(ParsingError):
    """Exception raised when content extraction fails."""
    pass


class MetadataExtractionError(ParsingError):
    """Exception raised when metadata extraction fails."""
    pass
