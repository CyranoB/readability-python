# Python Readability Project Brief

## Project Overview

The Python Readability project aims to create a Python port of the `go-readability` library, which is a Go implementation of the Readability algorithm. The Readability algorithm extracts the main content from HTML pages, removing navigation, ads, and other non-content elements, making it easier to read and process the actual content.

## Core Requirements

1. **High Fidelity Port**: Create a faithful port of the Go implementation to Python, maintaining the same functionality and behavior.
2. **Pythonic Implementation**: While maintaining fidelity to the original, use Python best practices and idioms where appropriate.
3. **Comprehensive Test Suite**: Migrate and adapt the existing test suite from the Go implementation to ensure the Python port behaves the same way.
4. **Performance Optimization**: Ensure the Python implementation is as performant as possible while maintaining readability and maintainability.

## Project Goals

1. **Library Implementation**: Create a Python library that can be used by other Python projects to extract the main content from HTML pages.
2. **CLI Tool**: Create a command-line interface for the library to allow users to extract content from HTML files or URLs.
3. **Documentation**: Provide comprehensive documentation for the library and CLI tool.
4. **Test Coverage**: Ensure high test coverage to maintain the quality of the codebase.

## Technical Constraints

1. **Python Version**: The library should be compatible with Python 3.6+.
2. **Dependencies**: Minimize external dependencies, but use established libraries where appropriate (e.g., BeautifulSoup for HTML parsing).
3. **API Compatibility**: The Python API should be similar to the Go API where it makes sense, but can be adapted to be more Pythonic.

## Implementation Phases

1. **Project Setup & Foundation**: Set up the project structure, tooling, and core data structures.
2. **Parsing & Preprocessing**: Implement HTML parsing and preprocessing functionality.
3. **Metadata Extraction**: Implement metadata extraction from HTML pages.
4. **Content Extraction & Scoring**: Implement the core content extraction and scoring algorithm.
5. **Post-processing & Output Generation**: Implement post-processing and output generation.
6. **Testing Infrastructure**: Set up comprehensive testing infrastructure.
7. **CLI Implementation**: Create a command-line interface for the library.
8. **Documentation & Packaging**: Create documentation and package the library for distribution.

## Success Criteria

1. **Test Passing**: All tests from the Go implementation should pass in the Python port.
2. **Performance**: The Python implementation should be reasonably performant compared to the Go implementation.
3. **Usability**: The library should be easy to use and integrate into other Python projects.
4. **Documentation**: The library should be well-documented with examples and usage instructions.
