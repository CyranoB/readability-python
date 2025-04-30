"""Data models for Python Readability.

This module defines the core data structures used by the Python Readability library,
including the Article class that represents the extracted content and metadata from
a web page, as well as exception classes for error handling.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from bs4 import Tag


@dataclass
class Article:
    """Article represents the final readable content extracted from a web page.
    
    This class is the primary output of the Readability parser and contains both
    the extracted content and metadata from the original web page. It mirrors the
    Article struct from the Go implementation to maintain compatibility.
    
    Example:
        ```python
        from readability import Readability
        
        parser = Readability()
        article, error = parser.parse(html_content, url="https://example.com/article")
        
        if article:
            print(f"Title: {article.title}")
            print(f"Author: {article.byline}")
            print(f"Content: {article.content[:100]}...")  # First 100 chars
        ```
    
    Attributes:
        url: The URL of the original web page, used for resolving relative links.
        title: The title of the article, extracted from metadata or content.
        byline: The author or authors of the article.
        node: The BeautifulSoup Tag object representing the main content node.
        content: The HTML string of the extracted content.
        text_content: The plain text version of the extracted content.
        length: The character count of the text content.
        excerpt: A short summary or description of the article.
        site_name: The name of the website or publication.
        image: URL of the main image associated with the article.
        favicon: URL of the favicon associated with the website.
        language: The detected language of the article.
        published_time: The datetime when the article was published.
        modified_time: The datetime when the article was last modified.
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
    """Base exception for parsing errors.
    
    This is the parent class for all parsing-related exceptions in the library.
    It can be used to catch any parsing error regardless of the specific type.
    
    Example:
        ```python
        try:
            article, error = parser.parse(html_content)
            if error:
                raise error
        except ParsingError as e:
            print(f"A parsing error occurred: {e}")
        ```
    """
    pass


class ExtractionError(ParsingError):
    """Exception raised when content extraction fails.
    
    This exception is raised when the parser is unable to extract the main
    content from the HTML document. This could happen if the document is
    malformed, empty, or doesn't contain any substantial content.
    
    Example:
        ```python
        try:
            article, error = parser.parse(html_content)
            if error:
                raise error
        except ExtractionError as e:
            print(f"Failed to extract content: {e}")
        ```
    """
    pass


class MetadataExtractionError(ParsingError):
    """Exception raised when metadata extraction fails.
    
    This exception is raised when the parser is unable to extract metadata
    (like title, author, publication date) from the HTML document. This could
    happen if the document doesn't contain the expected metadata tags or if
    they are malformed.
    
    Example:
        ```python
        try:
            article, error = parser.parse(html_content)
            if error:
                raise error
        except MetadataExtractionError as e:
            print(f"Failed to extract metadata: {e}")
        ```
    """
    pass
