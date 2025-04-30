"""Utility functions for Python Readability."""

from typing import Callable, Dict, List, Optional, TypeVar
from urllib.parse import ParseResult, urljoin, urlparse

T = TypeVar('T')


def index_of(array: List[T], key: T) -> int:
    """Return the position of the first occurrence of a specified value in a list.
    
    Args:
        array: The list to search in
        key: The value to search for
        
    Returns:
        The position of the first occurrence of the value, or -1 if not found
    """
    try:
        return array.index(key)
    except ValueError:
        return -1


def word_count(text: str) -> int:
    """Return the number of words in a string.
    
    Args:
        text: The string to count words in
        
    Returns:
        The number of words in the string
    """
    return len(text.split())


def char_count(text: str) -> int:
    """Return the number of characters in a string.
    
    Args:
        text: The string to count characters in
        
    Returns:
        The number of characters in the string
    """
    return len(text)


def is_valid_url(url: str) -> bool:
    """Check if a URL is valid.
    
    Args:
        url: The URL to check
        
    Returns:
        True if the URL is valid, False otherwise
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def to_absolute_uri(uri: str, base: Optional[ParseResult] = None) -> str:
    """Convert a URI to an absolute path based on a base URL.
    
    Args:
        uri: The URI to convert
        base: The base URL to resolve against
        
    Returns:
        The absolute URI
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
    
    Args:
        *args: The strings to check
        
    Returns:
        The first non-empty string, or an empty string if all are empty
    """
    for arg in args:
        if arg:
            return arg
    return ""


def list_to_dict(items: List[str]) -> Dict[str, bool]:
    """Convert a list of strings to a dictionary for fast lookup.
    
    Args:
        items: The list of strings to convert
        
    Returns:
        A dictionary with the strings as keys and True as values
    """
    return {item: True for item in items}


def str_filter(strings: List[str], filter_fn: Callable[[str], bool]) -> List[str]:
    """Filter a list of strings based on a predicate function.
    
    Args:
        strings: The list of strings to filter
        filter_fn: The predicate function to apply
        
    Returns:
        A new list containing only the strings that satisfy the predicate
    """
    return [s for s in strings if filter_fn(s)]


def trim(text: str) -> str:
    """Trim whitespace and normalize spaces in a string.
    
    Args:
        text: The string to trim
        
    Returns:
        The trimmed string
    """
    # Join multiple whitespace into a single space
    normalized = ' '.join(text.split())
    return normalized.strip()


def normalize_spaces(text: str) -> str:
    """Normalize spaces in a string.
    
    This is similar to trim() but doesn't strip leading/trailing spaces.
    
    Args:
        text: The string to normalize
        
    Returns:
        The normalized string
    """
    return ' '.join(text.split())
