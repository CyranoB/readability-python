# Readability Python

A high-fidelity Python port of the [go-readability](https://github.com/go-shiori/go-readability) library, which itself is a Go port of Mozilla's [Readability](https://github.com/mozilla/readability) library. This library extracts the main content from HTML pages, removing navigation, ads, and other non-content elements, making it easier to read and process the actual content.

## Features

- Extract the main article content from HTML pages
- Extract metadata (title, author, publication date, etc.)
- Convert relative URLs to absolute URLs
- Generate both HTML and plain text versions of the content
- Handle various edge cases (hidden elements, malformed HTML, etc.)
- Pythonic API with explicit error handling

## Installation

```bash
pip install readability-python
```

```bash
# Install from source
git clone https://github.com/CyranoB/readability-python.git
cd readability-python
pip install -e .

# With Poetry
poetry add readability-python
```

## Usage

### Basic Usage

```python
from readability import Readability

# Parse HTML content
parser = Readability()
article, error = parser.parse(html_content, url="https://example.com/article")

if error:
    print(f"Error: {error}")
else:
    # Access extracted content and metadata
    print(f"Title: {article.title}")
    print(f"Byline: {article.byline}")
    print(f"Content: {article.content}")  # HTML content
    print(f"Text Content: {article.text_content}")  # Plain text content
    print(f"Excerpt: {article.excerpt}")
    print(f"Site Name: {article.site_name}")
    print(f"Image: {article.image}")
    print(f"Favicon: {article.favicon}")
    print(f"Length: {article.length}")
    print(f"Published Time: {article.published_time}")
```

### CLI Usage

```bash
# Extract content from a URL
readability-python https://example.com/article --output article.html

# Extract content from a file
readability-python article.html --output extracted.html

# Output as JSON
readability-python https://example.com/article --format json --output article.json

# Output as plain text
readability-python https://example.com/article --format text --output article.txt
```

> **Note**: When specifying output files, it's recommended to use either absolute paths or paths within a dedicated output directory (e.g., `output/article.html`) to avoid cluttering your project directory. Output files in the root directory (like `extracted.html`) are automatically added to `.gitignore`.

## Testing

The library includes a comprehensive test suite to ensure compatibility with the original Go implementation. The tests are categorized by:

### Functional Areas
- HTML Parsing
- Metadata Extraction
- Content Identification
- Content Cleaning
- URL Handling
- Visibility Detection
- Text Normalization
- Real-world Websites

### Criticality Levels
- P0 (Critical) - Core functionality that must work
- P1 (High) - Important functionality with significant impact
- P2 (Medium) - Functionality that should work but has workarounds
- P3 (Low) - Nice-to-have functionality with minimal impact

### Test Types
- Basic - Tests for basic functionality
- Feature - Tests for specific features
- Edge Case - Tests for handling edge cases
- Real-world - Tests using real-world websites

To run the tests:

```bash
# Run all tests
pytest

# Run tests by functional area
pytest -m "area_html_parsing"

# Run tests by criticality
pytest -m "criticality_p0"

# Run tests by type
pytest -m "type_real_world"
```

## Test Coverage

The library has extensive test coverage across different functional areas and criticality levels:

| Functional Area | P0 | P1 | P2 | P3 | Total |
|----------------|----|----|----|----|-------|
| HTML Parsing | 0 | 0 | 2 | 0 | 2 |
| Metadata Extraction | 0 | 3 | 0 | 0 | 3 |
| Content Identification | 2 | 0 | 0 | 0 | 2 |
| Content Cleaning | 1 | 5 | 1 | 0 | 7 |
| URL Handling | 0 | 3 | 0 | 0 | 3 |
| Visibility Detection | 1 | 1 | 0 | 0 | 2 |
| Text Normalization | 0 | 1 | 3 | 0 | 4 |
| Real-world Websites | 4 | 1 | 2 | 7 | 14 |
| **Total** | **8** | **14** | **8** | **7** | **37** |

### Test Type Distribution

| Test Type | Count | Percentage |
|-----------|-------|------------|
| Basic | 2 | 5.4% |
| Feature | 14 | 37.8% |
| Edge Case | 7 | 18.9% |
| Real-world | 14 | 37.8% |

## Comparison with Go Implementation

This library aims to be a high-fidelity port of the [go-readability](https://github.com/go-shiori/go-readability) library, with the following considerations:

- Maintains the same functionality and behavior
- Uses Python best practices and idioms where appropriate
- Adapts the API to be more Pythonic while maintaining the same core functionality
- Uses BeautifulSoup for HTML parsing instead of Go's DOM implementation
- Maps Go's DOM traversal methods to BeautifulSoup's methods

## Development

### Requirements

- Python 3.6+
- Poetry (optional, for dependency management)

### Setup

```bash
# Clone the repository
git clone https://github.com/CyranoB/readability-python.git
cd readability-python

# Install dependencies with pip
pip install -e ".[dev]"

# Or with Poetry
poetry install
```

### Development Workflow

```bash
# Run tests
pytest

# Format code
black readability tests

# Lint code
ruff readability tests

# Type check
mypy readability
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Adding New Test Cases

1. Create a new directory in `tests/test-pages/` with a descriptive name
2. Add the following files to the directory:
   - `source.html` - The HTML to parse
   - `expected.html` - The expected content
   - `expected-metadata.json` - The expected metadata
3. Add the test case to `tests/test_categories.py` with appropriate categorization

## License

This project is licensed under the Apache 2.0 License - see the LICENSE file for details.
