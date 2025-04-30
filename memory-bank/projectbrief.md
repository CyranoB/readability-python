# Project Brief: Python Readability

## Overview
Python Readability is a port of the Mozilla Readability to Python using the `go-readability` as guideline. The goal is to create a high-fidelity Python implementation that follows Python best practices while maintaining the core functionality of the original Go library.

## Core Requirements
1. Port all functionality from `go-readability` to Python
2. Maintain high fidelity to the original implementation's behavior
3. Follow Python best practices (dataclasses, standard tooling)
4. Ensure comprehensive test coverage using the original test cases
5. Provide both a library API and CLI interface

## Project Goals
- Create a Python library that extracts the main content from web pages
- Maintain the same extraction quality as the Go version
- Make the library easy to use for Python developers
- Ensure the code is well-documented and maintainable
- Pass all test cases from the original Go implementation

## Key Features
- Extract the main content from HTML pages
- Remove clutter, ads, and irrelevant content
- Extract metadata (title, author, publication date, etc.)
- Provide both HTML and plain text output
- Support for various input formats (HTML string, bytes, URL)

## Success Criteria
- All test cases from the original Go implementation pass
- Code follows Python best practices
- Well-documented API and usage examples
- Comprehensive test coverage
- Functional CLI interface
