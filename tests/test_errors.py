"""Tests for the CLI error handling system."""

import io
import json
import sys
import unittest
from unittest import mock
from pathlib import Path

import pytest
import requests

from cli.errors import ErrorBoundary, ErrorType, with_error_boundary, ErrorBoundaryExit


# Simple test function at the module level for pytest discovery
def test_error_module_imports():
    """Simple test to verify module imports work."""
    assert hasattr(ErrorType, "SUCCESS")
    assert hasattr(ErrorBoundary, "__enter__")


class TestErrorType:
    """Test the ErrorType enum."""
    
    def test_error_types_exist(self):
        """Test that all expected error types are defined."""
        # Check that basic error types are defined
        assert ErrorType.SUCCESS.value == 0
        assert ErrorType.INPUT.value == 1
        assert ErrorType.NETWORK.value == 2
        assert ErrorType.PARSING.value == 3
        assert ErrorType.OUTPUT.value == 4
        assert ErrorType.UNKNOWN.value == 10
        
        # Check for additional error types
        assert ErrorType.PERMISSION is not None
        assert ErrorType.ENCODING is not None
        assert ErrorType.RESOURCE is not None
        assert ErrorType.TIMEOUT is not None
        assert ErrorType.VALIDATION is not None
    
    def test_error_types_are_unique(self):
        """Test that all error types have unique values."""
        values = [error_type.value for error_type in ErrorType]
        assert len(values) == len(set(values)), "Error type values are not unique"


class TestErrorBoundary:
    """Test the ErrorBoundary context manager using pytest style."""
    
    def test_normal_execution(self):
        """Test that normal execution proceeds without errors."""
        with ErrorBoundary("test_operation", ErrorType.UNKNOWN) as eb:
            result = 2 + 2
        
        assert result == 4
    
    def test_exception_handling(self):
        """Test that exceptions are properly caught."""
        with pytest.raises(ErrorBoundaryExit) as exc_info:
            with ErrorBoundary("test_operation", ErrorType.INPUT) as eb:
                raise ValueError("Test error")
        
        # Check the stored error message
        assert "Error in test_operation" in ErrorBoundary.last_error_message
        assert "Test error" in ErrorBoundary.last_error_message
        
        # Also check the exception attributes
        assert exc_info.value.error_type == ErrorType.INPUT
        assert "Test error" in str(exc_info.value)
    
    def test_continue_on_error(self):
        """Test that continue_on_error allows execution to continue."""
        with ErrorBoundary("test_operation", ErrorType.INPUT, continue_on_error=True) as eb:
            raise ValueError("Test error")
        
        # We should get here if continue_on_error works
        after_error = True
        
        # Check the stored error message instead of capturing stderr
        assert "Error in test_operation" in ErrorBoundary.last_error_message
        assert "Test error" in ErrorBoundary.last_error_message
        assert after_error
    
    def test_context_tracking(self):
        """Test that context is properly tracked and displayed."""
        with pytest.raises(ErrorBoundaryExit) as exc_info:
            with ErrorBoundary("test_operation", ErrorType.INPUT, verbose=True) as eb:
                eb.add_context("key1", "value1")
                eb.add_context("key2", 42)
                raise ValueError("Test error with context")
        
        # Check the stored error message
        assert "Context:" in ErrorBoundary.last_error_message
        assert "key1: value1" in ErrorBoundary.last_error_message
        assert "key2: 42" in ErrorBoundary.last_error_message
    
    def test_method_chaining(self):
        """Test that add_context supports method chaining."""
        with ErrorBoundary("test_operation", ErrorType.UNKNOWN) as eb:
            eb.add_context("key1", "value1").add_context("key2", "value2")
            
            assert eb.context["key1"] == "value1"
            assert eb.context["key2"] == "value2"
    
    def test_json_output_format(self):
        """Test that errors can be output in JSON format."""
        with pytest.raises(ErrorBoundaryExit) as exc_info:
            with ErrorBoundary("test_operation", ErrorType.INPUT, error_format="json") as eb:
                eb.add_context("key1", "value1")
                raise ValueError("Test error with JSON output")
        
        # Parse the stored error message as JSON
        error_json = json.loads(ErrorBoundary.last_error_message)
        
        assert error_json["operation"] == "test_operation"
        assert error_json["error_type"] == "INPUT"
        assert error_json["error_code"] == 1
        assert error_json["message"] == "Test error with JSON output"
        assert error_json["exception_type"] == "ValueError"
        
        # Check the exception itself
        assert exc_info.value.error_type == ErrorType.INPUT


class TestWithErrorBoundary:
    """Test the with_error_boundary decorator."""
    
    def test_decorator_basic_functionality(self):
        """Test that the decorator wraps a function with an error boundary."""
        
        @with_error_boundary(ErrorType.VALIDATION)
        def validate_number(n):
            if n < 0:
                raise ValueError("Number cannot be negative")
            return n * 2
        
        # Test with valid input
        assert validate_number(5) == 10
        
        # Test with invalid input
        with pytest.raises(SystemExit):
            validate_number(-5)
                
        # Check the stored error message
        assert "validate_number" in ErrorBoundary.last_error_message
        assert "Number cannot be negative" in ErrorBoundary.last_error_message
    
    def test_decorator_with_custom_name(self):
        """Test that the decorator allows custom operation names."""
        
        @with_error_boundary(ErrorType.VALIDATION, "custom_validation")
        def validate_number(n):
            if n < 0:
                raise ValueError("Number cannot be negative")
            return n * 2
        
        with pytest.raises(SystemExit):
            validate_number(-5)
                
        # Check the stored error message
        assert "custom_validation" in ErrorBoundary.last_error_message
        assert "validate_number" not in ErrorBoundary.last_error_message
    
    def test_decorator_passes_options(self):
        """Test that the decorator passes error handling options to the boundary."""
        
        @with_error_boundary(ErrorType.VALIDATION)
        def validate_with_options(n, verbose=False, continue_on_error=False, error_format="text"):
            if n < 0:
                raise ValueError("Number cannot be negative")
            return n * 2
        
        # Test with continue_on_error=True
        result = validate_with_options(-5, continue_on_error=True)
        # Function should return None when an error occurs but execution continues
        assert result is None
        assert "validate_with_options" in ErrorBoundary.last_error_message
        assert "Number cannot be negative" in ErrorBoundary.last_error_message
        
        # Test with error_format="json"
        with pytest.raises(SystemExit):
            validate_with_options(-5, error_format="json")
                
        # Parse the stored error message
        error_json = json.loads(ErrorBoundary.last_error_message)
        assert error_json["operation"] == "validate_with_options"
        assert error_json["message"] == "Number cannot be negative"


class TestRealScenarios:
    """Test error boundaries with real-world scenarios."""
    
    def test_file_not_found_scenario(self):
        """Test error handling for a file not found scenario (real filesystem)."""
        
        @with_error_boundary(ErrorType.INPUT)
        def read_nonexistent_file():
            with open("nonexistent_file.txt", "r") as f:
                return f.read()
        
        with pytest.raises(SystemExit) as exit_ctx:
            read_nonexistent_file()
        
        assert exit_ctx.value.code == ErrorType.INPUT.value
        assert "No such file or directory" in ErrorBoundary.last_error_message
    
    def test_file_not_found_scenario_mocked(self, mocker):
        """Test error handling for a file not found scenario with mocked filesystem."""
        
        # Setup the mock to raise FileNotFoundError
        mock_open = mocker.patch("builtins.open")
        file_path = "nonexistent_file.txt"
        mock_open.side_effect = FileNotFoundError(2, "No such file or directory", file_path)
        
        @with_error_boundary(ErrorType.INPUT)
        def read_nonexistent_file():
            with open(file_path, "r") as f:
                return f.read()
        
        with pytest.raises(SystemExit) as exit_ctx:
            read_nonexistent_file()
        
        assert exit_ctx.value.code == ErrorType.INPUT.value
        assert "No such file or directory" in ErrorBoundary.last_error_message
        
        # Verify the mock was called with the expected arguments
        mock_open.assert_called_once_with(file_path, "r")
    
    def test_network_error_scenario(self):
        """Test error handling for a network error scenario (real network)."""
        
        @with_error_boundary(ErrorType.NETWORK)
        def make_failed_request():
            response = requests.get("https://nonexistent.domain.invalid")
            return response.text
        
        with pytest.raises(SystemExit) as exit_ctx:
            make_failed_request()
        
        assert exit_ctx.value.code == ErrorType.NETWORK.value
        
        # Check that the error message contains a DNS failure reference
        assert any(msg in ErrorBoundary.last_error_message for msg in [
            "Name or service not known",
            "nodename nor servname provided",
            "Name resolution error",
            "getaddrinfo failed",
            "No address associated with hostname"
        ])
    
    def test_network_error_scenario_mocked(self, mocker):
        """Test error handling for a network error scenario with mocked requests."""
        
        # Mock the requests.get method
        mock_get = mocker.patch("requests.get")
        url = "https://nonexistent.domain.invalid"
        mock_get.side_effect = requests.exceptions.ConnectionError(
            "Failed to resolve 'nonexistent.domain.invalid' ([Errno 8] nodename nor servname provided, or not known)"
        )
        
        @with_error_boundary(ErrorType.NETWORK)
        def make_failed_request():
            response = requests.get(url)
            return response.text
        
        with pytest.raises(SystemExit) as exit_ctx:
            make_failed_request()
        
        assert exit_ctx.value.code == ErrorType.NETWORK.value
        assert "nonexistent.domain.invalid" in ErrorBoundary.last_error_message
        
        # Verify the mock was called with the expected URL
        mock_get.assert_called_once_with(url)
        
    @pytest.mark.parametrize("exception,expected_text", [
        (requests.exceptions.ConnectionError("connection error"), "connection error"),
        (requests.exceptions.Timeout("timeout error"), "timeout error"),
        (requests.exceptions.TooManyRedirects("too many redirects"), "too many redirects"),
        (requests.exceptions.RequestException("general error"), "general error"),
    ])
    def test_network_error_variations(self, mocker, exception, expected_text):
        """Test handling of various network error types."""
        mock_get = mocker.patch("requests.get")
        mock_get.side_effect = exception
        url = "https://example.com"
        
        @with_error_boundary(ErrorType.NETWORK)
        def make_request():
            return requests.get(url).text
        
        with pytest.raises(SystemExit) as exit_ctx:
            make_request()
        
        assert exit_ctx.value.code == ErrorType.NETWORK.value
        assert expected_text in ErrorBoundary.last_error_message.lower()
        mock_get.assert_called_once_with(url)
    
    @pytest.mark.parametrize("exception,expected_code", [
        (FileNotFoundError(2, "No such file", "test.txt"), ErrorType.INPUT.value),
        (PermissionError(13, "Permission denied", "test.txt"), ErrorType.PERMISSION.value),
        (IsADirectoryError(21, "Is a directory", "test.txt"), ErrorType.INPUT.value),
    ])
    def test_file_error_variations(self, mocker, exception, expected_code):
        """Test handling of various file error types."""
        mock_open = mocker.patch("builtins.open")
        mock_open.side_effect = exception
        file_path = "test.txt"
        
        # We use INPUT as the initial type, but the handler may override it
        # based on the specific exception type
        @with_error_boundary(ErrorType.INPUT)
        def read_file():
            with open(file_path, "r") as f:
                return f.read()
        
        with pytest.raises(SystemExit) as exit_ctx:
            read_file()
            
        # The exit code should match the error type we expect
        assert exit_ctx.value.code == expected_code
        
        # The error message should contain info about the exception
        assert str(exception.strerror).lower() in ErrorBoundary.last_error_message.lower()
        mock_open.assert_called_once_with(file_path, "r")
    
    def test_nested_error_boundaries(self):
        """Test that nested error boundaries work correctly."""
        error_messages = []
        
        def outer_function():
            # Use continue_on_error to catch inner errors
            with ErrorBoundary("outer", ErrorType.UNKNOWN, continue_on_error=True) as eb_outer:
                eb_outer.add_context("level", "outer")
                
                # This try/except is just a safeguard, with our ErrorBoundaryExit approach
                # the exception should be caught by the boundary's __exit__ method
                try:
                    inner_function()
                except ErrorBoundaryExit as e:
                    # We should see this exception from inner function
                    error_messages.append(f"Caught inner error: {e}")
                
                # This should still execute even after inner error
                return "Outer completed"
        
        def inner_function():
            with ErrorBoundary("inner", ErrorType.VALIDATION) as eb_inner:
                eb_inner.add_context("level", "inner")
                raise ValueError("Inner validation error")
        
        # Reset the last error message before our test
        ErrorBoundary.last_error_message = None
        
        # The inner error boundary should raise ErrorBoundaryExit
        # and outer should catch it since continue_on_error=True
        result = outer_function()
        
        # Check that execution continued in the outer function
        assert result == "Outer completed"
        
        # Check that error messages were recorded properly
        assert len(error_messages) > 0
        assert "Caught inner error" in error_messages[0]
        
        # Check the last error message (should be from the inner boundary)
        assert ErrorBoundary.last_error_message is not None
        assert "Inner validation error" in ErrorBoundary.last_error_message
