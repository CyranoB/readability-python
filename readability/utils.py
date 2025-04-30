"""Utility functions for Python Readability.

This module provides a collection of utility functions used throughout the
Python Readability library. These functions handle common operations like
string manipulation, URL processing, and data structure conversions.

The functions in this module are designed to be simple, focused, and reusable.
They abstract away common operations to make the main code more readable and
maintainable.
"""

from typing import Callable, Dict, List, Optional, TypeVar
from urllib.parse import ParseResult, urljoin, urlparse

T = TypeVar('T')


def index_of(array: List[T], key: T) -> int:
    """Return the position of the first occurrence of a specified value in a list.
    
    This function mimics JavaScript's Array.indexOf() method. It returns the
    index of the first occurrence of the specified value in the list, or -1 if
    the value is not found.
    
    Args:
        array: The list to search in
        key: The value to search for
        
    Returns:
        The position of the first occurrence of the value, or -1 if not found
        
    Example:
        ```python
        fruits = ["apple", "banana", "orange", "banana"]
        position = index_of(fruits, "banana")  # Returns 1
        not_found = index_of(fruits, "grape")  # Returns -1
        ```
    """
    try:
        return array.index(key)
    except ValueError:
        return -1


def word_count(text: str) -> int:
    """Return the number of words in a string.
    
    Words are considered to be separated by whitespace. This is a simple
    implementation that splits the string on whitespace and counts the
    resulting items.
    
    Args:
        text: The string to count words in
        
    Returns:
        The number of words in the string
        
    Example:
        ```python
        count = word_count("Hello world!")  # Returns 2
        count = word_count("This is a test.")  # Returns 4
        ```
    """
    return len(text.split())


def char_count(text: str) -> int:
    """Return the number of characters in a string.
    
    This function simply returns the length of the input string.
    
    Args:
        text: The string to count characters in
        
    Returns:
        The number of characters in the string
        
    Example:
        ```python
        count = char_count("Hello")  # Returns 5
        count = char_count("Hello world!")  # Returns 12
        ```
    """
    return len(text)


def is_valid_url(url: str) -> bool:
    """Check if a URL is valid.
    
    A URL is considered valid if it has both a scheme (e.g., http, https)
    and a network location (e.g., example.com).
    
    Args:
        url: The URL to check
        
    Returns:
        True if the URL is valid, False otherwise
        
    Example:
        ```python
        is_valid = is_valid_url("https://example.com")  # Returns True
        is_valid = is_valid_url("example.com")  # Returns False (no scheme)
        is_valid = is_valid_url("https://")  # Returns False (no netloc)
        ```
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def to_absolute_uri(uri: str, base: Optional[ParseResult] = None) -> str:
    """Convert a URI to an absolute path based on a base URL.
    
    This function resolves relative URIs against a base URL to create
    absolute URIs. It handles special cases like hash fragments and
    data URIs.
    
    Args:
        uri: The URI to convert
        base: The base URL to resolve against (as a ParseResult object)
        
    Returns:
        The absolute URI, or the original URI if it cannot be converted
        or if no base URL is provided
        
    Example:
        ```python
        from urllib.parse import urlparse
        
        base = urlparse("https://example.com/articles/")
        abs_uri = to_absolute_uri("image.jpg", base)  # Returns "https://example.com/articles/image.jpg"
        abs_uri = to_absolute_uri("/images/logo.png", base)  # Returns "https://example.com/images/logo.png"
        abs_uri = to_absolute_uri("#section1", base)  # Returns "#section1" (hash fragments are preserved)
        ```
    """
    if not uri or not base:
        return uri
    
    # If it is a hash tag, return as it is
    if uri.startswith('#'):
        return uri
    
    # If it is a data URI, return as it is
    if uri.startswith('data:'):
        return uri
    
    # If it is already an absolute URL, return as it is
    try:
        parsed = urlparse(uri)
        if parsed.scheme and parsed.netloc:
            return uri
    except Exception:
        return uri
    
    # Otherwise, resolve against base URI
    try:
        base_url = f"{base.scheme}://{base.netloc}{base.path}"
        return urljoin(base_url, uri)
    except Exception:
        return uri


def str_or(*args: str) -> str:
    """Return the first non-empty string in a list of strings.
    
    This function is useful for providing fallbacks when extracting
    metadata from multiple potential sources.
    
    Args:
        *args: The strings to check
        
    Returns:
        The first non-empty string, or an empty string if all are empty
        
    Example:
        ```python
        # Try to get title from multiple sources
        title = str_or(metadata.get("og:title"), metadata.get("twitter:title"), "Default Title")
        ```
    """
    for arg in args:
        if arg:
            return arg
    return ""


def list_to_dict(items: List[str]) -> Dict[str, bool]:
    """Convert a list of strings to a dictionary for fast lookup.
    
    This function creates a dictionary where the keys are the strings
    from the input list and the values are all True. This is useful
    for efficient membership testing.
    
    Args:
        items: The list of strings to convert
        
    Returns:
        A dictionary with the strings as keys and True as values
        
    Example:
        ```python
        # Create a set-like dictionary for fast lookups
        block_tags = list_to_dict(["div", "p", "table", "pre"])
        
        # Check if a tag is a block tag
        is_block = "div" in block_tags  # True
        ```
    """
    return {item: True for item in items}


def str_filter(strings: List[str], filter_fn: Callable[[str], bool]) -> List[str]:
    """Filter a list of strings based on a predicate function.
    
    This function applies a filter function to each string in the list
    and returns a new list containing only the strings that satisfy
    the predicate.
    
    Args:
        strings: The list of strings to filter
        filter_fn: The predicate function to apply
        
    Returns:
        A new list containing only the strings that satisfy the predicate
        
    Example:
        ```python
        # Filter out empty strings
        non_empty = str_filter(["a", "", "b", "c", ""], lambda s: len(s) > 0)
        # Returns ["a", "b", "c"]
        
        # Filter strings by length
        long_strings = str_filter(["a", "abc", "abcdef"], lambda s: len(s) > 3)
        # Returns ["abcdef"]
        ```
    """
    return [s for s in strings if filter_fn(s)]


def trim(text: str) -> str:
    """Trim whitespace and normalize spaces in a string.
    
    This function removes leading and trailing whitespace and replaces
    all internal whitespace sequences with a single space.
    
    Args:
        text: The string to trim
        
    Returns:
        The trimmed string
        
    Example:
        ```python
        trimmed = trim("  Hello   world!  ")  # Returns "Hello world!"
        trimmed = trim("\n\tMultiple\n\nlines\t")  # Returns "Multiple lines"
        ```
    """
    # Join multiple whitespace into a single space
    normalized = ' '.join(text.split())
    return normalized.strip()


def normalize_spaces(text: str) -> str:
    """Normalize spaces in a string.
    
    This function replaces all whitespace sequences with a single space,
    but unlike trim(), it doesn't strip leading/trailing spaces.
    
    Args:
        text: The string to normalize
        
    Returns:
        The normalized string
        
    Example:
        ```python
        normalized = normalize_spaces("  Hello   world!  ")  # Returns " Hello world! "
        normalized = normalize_spaces("\n\tMultiple\n\nlines\t")  # Returns " Multiple lines "
        ```
    """
    return ' '.join(text.split())
