"""Tests for utility functions."""

import unittest
from urllib.parse import urlparse

from readability.utils import (
    index_of,
    word_count,
    char_count,
    is_valid_url,
    to_absolute_uri,
    str_or,
    list_to_dict,
    str_filter,
    trim,
    normalize_spaces
)


class TestIndexOf(unittest.TestCase):
    """Test the index_of function."""
    
    def test_element_exists(self):
        """Test finding an element that exists in the list."""
        # Test with strings
        self.assertEqual(index_of(["a", "b", "c"], "b"), 1)
        
        # Test with integers
        self.assertEqual(index_of([10, 20, 30, 40], 30), 2)
        
        # Test with mixed types
        self.assertEqual(index_of([1, "two", 3.0], "two"), 1)
    
    def test_element_not_exists(self):
        """Test finding an element that doesn't exist in the list."""
        # Test with empty list
        self.assertEqual(index_of([], "a"), -1)
        
        # Test with non-empty list
        self.assertEqual(index_of(["a", "b", "c"], "d"), -1)
        
        # Test with integers
        self.assertEqual(index_of([10, 20, 30], 40), -1)
    
    def test_first_occurrence(self):
        """Test that only the first occurrence is returned."""
        # Test with multiple occurrences
        self.assertEqual(index_of(["a", "b", "a", "c"], "a"), 0)
        self.assertEqual(index_of([10, 20, 10, 30], 10), 0)


class TestWordCount(unittest.TestCase):
    """Test the word_count function."""
    
    def test_empty_string(self):
        """Test word count for empty string."""
        self.assertEqual(word_count(""), 0)
    
    def test_single_word(self):
        """Test word count for a single word."""
        self.assertEqual(word_count("hello"), 1)
    
    def test_multiple_words(self):
        """Test word count for multiple words."""
        self.assertEqual(word_count("hello world"), 2)
        self.assertEqual(word_count("this is a test"), 4)
    
    def test_multiple_spaces(self):
        """Test word count with multiple spaces between words."""
        self.assertEqual(word_count("hello   world"), 2)
        self.assertEqual(word_count("  leading and trailing  spaces  "), 4)
    
    def test_special_characters(self):
        """Test word count with special characters."""
        self.assertEqual(word_count("hello, world!"), 2)
        self.assertEqual(word_count("hyphenated-word"), 1)
    
    def test_newlines_and_tabs(self):
        """Test word count with newlines and tabs."""
        self.assertEqual(word_count("hello\nworld"), 2)
        self.assertEqual(word_count("hello\tworld"), 2)
        self.assertEqual(word_count("multiple\n\twhitespace\n\ncharacters"), 3)


class TestCharCount(unittest.TestCase):
    """Test the char_count function."""
    
    def test_empty_string(self):
        """Test character count for empty string."""
        self.assertEqual(char_count(""), 0)
    
    def test_simple_string(self):
        """Test character count for simple string."""
        self.assertEqual(char_count("hello"), 5)
        self.assertEqual(char_count("hello world"), 11)  # Including the space
    
    def test_special_characters(self):
        """Test character count with special characters."""
        self.assertEqual(char_count("hello\nworld"), 11)  # Including the newline
        self.assertEqual(char_count("emoji 😊"), 7)  # Unicode characters may count differently


class TestIsValidUrl(unittest.TestCase):
    """Test the is_valid_url function."""
    
    def test_valid_urls(self):
        """Test valid URLs."""
        self.assertTrue(is_valid_url("http://example.com"))
        self.assertTrue(is_valid_url("https://example.com"))
        self.assertTrue(is_valid_url("https://www.example.com/path?query=value#fragment"))
        self.assertTrue(is_valid_url("ftp://files.example.com"))
    
    def test_invalid_urls(self):
        """Test invalid URLs."""
        # Missing scheme
        self.assertFalse(is_valid_url("example.com"))
        
        # Missing netloc
        self.assertFalse(is_valid_url("https://"))
        
        # Invalid format
        self.assertFalse(is_valid_url("not a url"))
        
        # Empty string
        self.assertFalse(is_valid_url(""))
    
    def test_edge_cases(self):
        """Test edge cases for URL validation."""
        # IP addresses
        self.assertTrue(is_valid_url("http://127.0.0.1"))
        self.assertTrue(is_valid_url("http://192.168.1.1:8080"))
        
        # Note: file:/// URLs might not work with urlparse correctly
        # Depends on implementation


class TestToAbsoluteUri(unittest.TestCase):
    """Test the to_absolute_uri function."""
    
    def test_empty_inputs(self):
        """Test with empty inputs."""
        self.assertEqual(to_absolute_uri("", None), "")
        self.assertEqual(to_absolute_uri(None, None), None)
        
        # URI without base
        base = urlparse("https://example.com/articles/")
        self.assertEqual(to_absolute_uri("", base), "")
    
    def test_hash_fragment(self):
        """Test with hash fragment."""
        base = urlparse("https://example.com/articles/")
        self.assertEqual(to_absolute_uri("#section1", base), "#section1")
    
    def test_data_uri(self):
        """Test with data URI."""
        base = urlparse("https://example.com/articles/")
        data_uri = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+P+/HgAFeAJ5gJ2CfQAAAABJRU5ErkJggg=="
        self.assertEqual(to_absolute_uri(data_uri, base), data_uri)
    
    def test_absolute_url(self):
        """Test with already absolute URL."""
        base = urlparse("https://example.com/articles/")
        self.assertEqual(to_absolute_uri("https://other.com/page", base), "https://other.com/page")
    
    def test_relative_path(self):
        """Test with relative path."""
        base = urlparse("https://example.com/articles/")
        self.assertEqual(to_absolute_uri("image.jpg", base), "https://example.com/articles/image.jpg")
        self.assertEqual(to_absolute_uri("../images/logo.png", base), "https://example.com/images/logo.png")
    
    def test_absolute_path(self):
        """Test with absolute path (root-relative)."""
        base = urlparse("https://example.com/articles/")
        self.assertEqual(to_absolute_uri("/images/logo.png", base), "https://example.com/images/logo.png")
    
    def test_exception_handling(self):
        """Test exception handling."""
        # Modified to test with a URL that may cause issues
        base = urlparse("https://example.com/articles/")
        
        # Test with a potentially problematic URL
        result = to_absolute_uri("////weird-url", base)
        # Just verify it doesn't raise an exception and returns something
        self.assertIsInstance(result, str)


class TestStrOr(unittest.TestCase):
    """Test the str_or function."""
    
    def test_empty_args(self):
        """Test with no arguments."""
        self.assertEqual(str_or(), "")
    
    def test_single_argument(self):
        """Test with a single argument."""
        self.assertEqual(str_or("hello"), "hello")
        self.assertEqual(str_or(""), "")
    
    def test_multiple_arguments(self):
        """Test with multiple arguments."""
        self.assertEqual(str_or("", "", "hello", "world"), "hello")
        self.assertEqual(str_or(None, "", "hello"), "hello")
        self.assertEqual(str_or(None, False, 0, "hello"), "hello")
    
    def test_all_empty(self):
        """Test when all arguments are empty."""
        self.assertEqual(str_or("", "", ""), "")
        self.assertEqual(str_or(None, None), "")
    
    def test_non_string_values(self):
        """Test with non-string values that evaluate to True."""
        # The str_or function likely returns the first non-empty value as-is (without str conversion)
        self.assertEqual(str_or("", 123), 123)
        self.assertEqual(str_or("", True), True)
        self.assertEqual(str_or("", [1, 2, 3]), [1, 2, 3])


class TestListToDict(unittest.TestCase):
    """Test the list_to_dict function."""
    
    def test_empty_list(self):
        """Test with empty list."""
        self.assertEqual(list_to_dict([]), {})
    
    def test_string_list(self):
        """Test with list of strings."""
        result = list_to_dict(["a", "b", "c"])
        self.assertEqual(result, {"a": True, "b": True, "c": True})
        
        # Check membership operations
        self.assertTrue("a" in result)
        self.assertTrue("b" in result)
        self.assertTrue("c" in result)
        self.assertFalse("d" in result)
    
    def test_mixed_list(self):
        """Test with mixed types."""
        result = list_to_dict([1, "two", 3.0])
        self.assertEqual(result, {1: True, "two": True, 3.0: True})
        
        # Check membership operations
        self.assertTrue(1 in result)
        self.assertTrue("two" in result)
        self.assertTrue(3.0 in result)
        self.assertFalse(2 in result)
    
    def test_duplicate_items(self):
        """Test with duplicate items in the list."""
        result = list_to_dict(["a", "b", "a"])
        self.assertEqual(result, {"a": True, "b": True})
        self.assertEqual(len(result), 2)  # Should have 2 unique keys


class TestStrFilter(unittest.TestCase):
    """Test the str_filter function."""
    
    def test_empty_list(self):
        """Test with empty list."""
        result = str_filter([], lambda s: len(s) > 0)
        self.assertEqual(result, [])
    
    def test_filter_by_length(self):
        """Test filtering by string length."""
        # Filter strings longer than 3 characters
        result = str_filter(["a", "ab", "abc", "abcd", "abcde"], lambda s: len(s) > 3)
        self.assertEqual(result, ["abcd", "abcde"])
        
        # Filter empty strings
        result = str_filter(["", "a", "", "b", ""], lambda s: s)
        self.assertEqual(result, ["a", "b"])
    
    def test_filter_by_content(self):
        """Test filtering by string content."""
        # Filter strings containing 'a'
        result = str_filter(["apple", "banana", "orange", "grape"], lambda s: "a" in s)
        self.assertEqual(result, ["apple", "banana", "orange", "grape"])
        
        # Filter strings containing 'e'
        result = str_filter(["apple", "banana", "orange", "grape"], lambda s: "e" in s)
        self.assertEqual(result, ["apple", "orange", "grape"])
    
    def test_complex_filter(self):
        """Test with more complex filter functions."""
        # Filter strings that start with 'a' and are longer than 4 characters
        result = str_filter(
            ["apple", "ant", "banana", "avocado"],
            lambda s: s.startswith("a") and len(s) > 4
        )
        self.assertEqual(result, ["apple", "avocado"])


class TestTrim(unittest.TestCase):
    """Test the trim function."""
    
    def test_empty_string(self):
        """Test with empty string."""
        self.assertEqual(trim(""), "")
    
    def test_no_whitespace(self):
        """Test with string without whitespace."""
        self.assertEqual(trim("hello"), "hello")
    
    def test_leading_trailing_whitespace(self):
        """Test with leading and trailing whitespace."""
        self.assertEqual(trim("  hello  "), "hello")
        self.assertEqual(trim("\n\thello\n\t"), "hello")
    
    def test_internal_whitespace(self):
        """Test with internal whitespace."""
        self.assertEqual(trim("hello  world"), "hello world")
        self.assertEqual(trim("multiple   spaces   between   words"), "multiple spaces between words")
    
    def test_mixed_whitespace(self):
        """Test with mixed whitespace types."""
        self.assertEqual(trim("  hello\n\tworld  "), "hello world")
        self.assertEqual(trim("\n\t  mixed\nwhitespace\t\r\nexample  \n"), "mixed whitespace example")


class TestNormalizeSpaces(unittest.TestCase):
    """Test the normalize_spaces function."""
    
    def test_empty_string(self):
        """Test with empty string."""
        self.assertEqual(normalize_spaces(""), "")
    
    def test_no_whitespace(self):
        """Test with string without whitespace."""
        self.assertEqual(normalize_spaces("hello"), "hello")
    
    def test_leading_trailing_whitespace(self):
        """Test with leading and trailing whitespace."""
        # The implementation might be using split() which also trims leading/trailing spaces
        self.assertEqual(normalize_spaces("  hello  "), "hello")
        # Actually similar to trim() in implementation
    
    def test_internal_whitespace(self):
        """Test with internal whitespace."""
        self.assertEqual(normalize_spaces("hello   world"), "hello world")
        self.assertEqual(normalize_spaces("multiple    spaces"), "multiple spaces")
    
    def test_mixed_whitespace(self):
        """Test with mixed whitespace types."""
        self.assertEqual(normalize_spaces("hello\n\tworld"), "hello world")
        self.assertEqual(normalize_spaces("\n\tmixed\nwhitespace\texample\n"), "mixed whitespace example")
