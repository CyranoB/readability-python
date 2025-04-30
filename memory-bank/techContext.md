# Technical Context: Python Readability

## Technologies Used

### Core Technologies
- **Python 3.8+**: Base language for implementation
- **BeautifulSoup4**: HTML parsing and manipulation
- **lxml**: XML/HTML parser (used as BeautifulSoup's parser)
- **python-dateutil**: For parsing and handling dates in metadata
- **requests** (optional): For fetching URLs in CLI mode

### Development Tools
- **Poetry**: Dependency management and packaging
- **pytest**: Testing framework
- **black**: Code formatting
- **ruff/flake8**: Linting
- **Git**: Version control

## Development Setup

### Project Structure
```
python-readability/
├── readability/           # Main library code
│   ├── __init__.py        # Package exports
│   ├── models.py          # Data models (Article class)
│   ├── parser.py          # Core parsing logic
│   ├── regexps.py         # Regular expressions
│   └── utils.py           # Utility functions
├── cli/                   # Command-line interface
│   ├── __init__.py
│   └── main.py            # CLI entry point
├── tests/                 # Test suite
│   ├── conftest.py        # Test configuration
│   ├── test_readability.py # Main tests
│   └── test-pages/        # Test cases from go-readability
├── pyproject.toml         # Project configuration
└── README.md              # Documentation
```

### Environment Setup
1. Python 3.8+ installed
2. Poetry installed for dependency management
3. Development dependencies installed via `poetry install`

## Technical Constraints

### Compatibility
- Must maintain behavioral compatibility with the original Go implementation
- Must pass all test cases from the original Go implementation
- Should support the same input formats and options as the Go version

### Performance
- Should have comparable performance to the Go implementation
- Should handle large HTML documents efficiently

### Dependencies
- Minimize external dependencies to keep the library lightweight
- Core dependencies:
  - beautifulsoup4: HTML parsing
  - lxml: Parser backend for BeautifulSoup
  - python-dateutil: Date parsing for metadata

### API Design
- Should provide a Pythonic API while maintaining compatibility with Go version
- Should use Python idioms and best practices (dataclasses, type hints, etc.)
- Should follow PEP 8 style guidelines

## Technical Challenges

### DOM Traversal Mapping
- Go implementation uses specific DOM traversal methods
- Need to map these to BeautifulSoup equivalents
- Ensure consistent behavior across different HTML structures

### Regular Expression Translation
- Go uses RE2 regular expression syntax
- Need to translate these to Python's re syntax
- Ensure pattern matching behavior is consistent

### Scoring Algorithm
- Complex heuristics for scoring content nodes
- Need to ensure Python implementation produces the same scores
- Small differences in scoring can lead to different extraction results

### Error Handling
- Go uses explicit error returns
- Python typically uses exceptions
- Need to design an error handling strategy that works well in Python while maintaining compatibility

## Testing Strategy

### Test Cases
- Reuse test cases from the original Go implementation
- Each test case consists of:
  - `source.html`: Input HTML
  - `expected.html`: Expected output HTML
  - `expected-metadata.json`: Expected metadata

### Test Infrastructure
- Use pytest for running tests
- Parameterized tests to run the same test logic against multiple test cases
- Helpers for loading test cases and comparing results

### Test Coverage
- Aim for high test coverage (90%+)
- Focus on testing edge cases and complex logic
- Include tests for error handling and edge cases
