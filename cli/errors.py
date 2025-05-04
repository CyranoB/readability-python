#!/usr/bin/env python3
"""Error handling system for CLI operations.

This module provides a structured approach to error handling in CLI operations using
an error boundary pattern. It helps with consistent error reporting, context capturing,
and appropriate error responses.
"""

import sys
import json
import contextlib
from enum import Enum
from typing import Any, Dict, Optional, TextIO, Callable, Union, Type


class ErrorBoundaryExit(Exception):
    """Special exception raised by ErrorBoundary to allow proper nesting."""
    
    def __init__(self, error_type: 'ErrorType', message: str):
        self.error_type = error_type
        self.message = message
        super().__init__(message)


class ErrorType(Enum):
    """Classification of error types with corresponding exit codes."""
    
    SUCCESS = 0
    INPUT = 1             # Input-related errors (file not found, invalid input)
    NETWORK = 2           # Network errors (connection issues, timeouts)
    PARSING = 3           # Content parsing errors
    OUTPUT = 4            # Output-related errors (cannot write to file)
    PERMISSION = 5        # Permission errors (file access, etc.)
    ENCODING = 6          # Encoding/decoding errors
    RESOURCE = 7          # Resource exhaustion (memory, disk space)
    TIMEOUT = 8           # Operation timeout
    VALIDATION = 9        # Validation errors
    UNKNOWN = 10          # Unclassified errors
    

class ErrorBoundary:
    """Context manager for handling errors in a consistent way.
    
    The ErrorBoundary class implements a context manager that can be used to wrap
    operations that might fail. It captures error context, formats error messages,
    and handles error reporting and exit codes.
    
    Example:
        ```python
        with ErrorBoundary("fetch_content", ErrorType.NETWORK) as eb:
            eb.add_context("url", "https://example.com")
            # Code that might raise exceptions
            response = requests.get(url, timeout=timeout)
        ```
    """
    
    # Class-level attribute to store the last error for testing
    last_error = None
    last_error_message = None  # For storing the string representation
    
    def __init__(self, operation_name: str, error_type: ErrorType = ErrorType.UNKNOWN, 
                 verbose: bool = False, continue_on_error: bool = False,
                 error_format: str = "text", stderr: TextIO = sys.stderr):
        """Initialize error boundary.
        
        Args:
            operation_name: Name of the operation being performed
            error_type: Type of error this boundary handles
            verbose: Whether to include detailed information in error messages
            continue_on_error: Whether to continue execution after an error
            error_format: Format for error messages ("text" or "json")
            stderr: Stream to write error messages to
        """
        self.operation_name = operation_name
        self.error_type = error_type
        self.verbose = verbose
        self.continue_on_error = continue_on_error
        self.error_format = error_format
        self.stderr = stderr
        self.context: Dict[str, Any] = {}
    
    def __enter__(self):
        """Enter the context manager."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context manager, handling any exceptions.
        
        Args:
            exc_type: Type of exception raised, if any
            exc_val: Exception instance raised, if any
            exc_tb: Traceback for the exception, if any
            
        Returns:
            Boolean indicating whether the exception was handled
        """
        if exc_type is not None:
            self.handle_error(exc_val)
            return self.continue_on_error
        return False
    
    def add_context(self, key: str, value: Any) -> 'ErrorBoundary':
        """Add context information to the error boundary.
        
        Args:
            key: Context key
            value: Context value
            
        Returns:
            The error boundary instance for chaining
        """
        self.context[key] = value
        return self
    
    def handle_error(self, exception: Exception) -> None:
        """Handle an exception.
        
        Args:
            exception: The exception to handle
        """
        # Check if this is already an ErrorBoundaryExit - avoid re-wrapping
        if isinstance(exception, ErrorBoundaryExit):
            # Pass through the error but report it at this level too
            error_info = {
                "operation": self.operation_name,
                "error_type": exception.error_type.name,
                "error_code": exception.error_type.value,
                "message": str(exception.error_type.value),  # Use the error code as message
                "exception_type": "ErrorBoundaryExit",
            }
            self.report_error(error_info)
            
            if not self.continue_on_error:
                # Re-raise the same boundary exit for outer handlers
                raise exception
            return
        
        # Determine the most appropriate error type based on the exception
        error_type = self.error_type
        if isinstance(exception, PermissionError):
            error_type = ErrorType.PERMISSION
        elif isinstance(exception, TimeoutError):
            error_type = ErrorType.TIMEOUT
        # Add more mappings as needed
        
        # Normal exception handling
        error_info = {
            "operation": self.operation_name,
            "error_type": error_type.name,
            "error_code": error_type.value,
            "message": str(exception),
            "exception_type": exception.__class__.__name__,
        }
        
        if self.verbose:
            error_info["context"] = self.context
        
        self.report_error(error_info)
        
        if not self.continue_on_error:
            # Instead of sys.exit(), raise our custom exception
            # This allows for proper nested error boundary handling
            raise ErrorBoundaryExit(error_type, str(exception))
    
    def report_error(self, error_info: Dict[str, Any]) -> None:
        """Report an error.
        
        Args:
            error_info: Information about the error
        """
        # Store error info for testing
        ErrorBoundary.last_error = error_info
        
        if self.error_format == "json":
            self._report_json(error_info)
        else:
            self._report_text(error_info)
    
    def _report_json(self, error_info: Dict[str, Any]) -> None:
        """Report an error in JSON format.
        
        Args:
            error_info: Information about the error
        """
        json_output = json.dumps(error_info, indent=2)
        ErrorBoundary.last_error_message = json_output  # Store for testing
        print(json_output, file=self.stderr)
    
    def _report_text(self, error_info: Dict[str, Any]) -> None:
        """Report an error in text format.
        
        Args:
            error_info: Information about the error
        """
        # Build the message
        error_lines = [f"Error in {error_info['operation']}: {error_info['message']}"]
        
        if self.verbose and "context" in error_info:
            error_lines.append("\nContext:")
            for key, value in error_info["context"].items():
                error_lines.append(f"  {key}: {value}")
        
        if "suggestion" in error_info:
            error_lines.append(f"\nSuggestion: {error_info['suggestion']}")
        
        # Save the complete message for testing
        ErrorBoundary.last_error_message = "\n".join(error_lines)
        
        # Output to stderr
        print(ErrorBoundary.last_error_message, file=self.stderr)


def with_error_boundary(error_type: ErrorType, operation_name: Optional[str] = None):
    """Decorator to wrap a function with an error boundary.
    
    Args:
        error_type: Type of error this boundary handles
        operation_name: Name of the operation being performed. If not provided,
                       the function name will be used.
    
    Returns:
        Decorated function
    """
    def decorator(func: Callable):
        nonlocal operation_name
        if operation_name is None:
            operation_name = func.__name__
            
        def wrapper(*args, **kwargs):
            verbose = kwargs.pop("verbose", False)
            continue_on_error = kwargs.pop("continue_on_error", False)
            error_format = kwargs.pop("error_format", "text")
            
            try:
                with ErrorBoundary(operation_name, error_type, verbose, continue_on_error, error_format) as eb:
                    return func(*args, **kwargs)
            except ErrorBoundaryExit as e:
                # At the top level, convert the error boundary exit to a system exit
                sys.exit(e.error_type.value)
                
        return wrapper
    return decorator
