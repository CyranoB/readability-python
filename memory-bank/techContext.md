# Technical Context for Python Readability

## Technologies Used

### Core Technologies

1. **Python 3.8+**: The library is implemented in Python 3.8+ to ensure compatibility with modern Python projects while leveraging newer language features.
2. **BeautifulSoup4**: Used for HTML parsing and DOM manipulation, with the lxml parser for performance.
3. **lxml**: Used as the HTML parser backend for BeautifulSoup.
4. **python-dateutil**: Used for parsing and handling dates in metadata extraction.
5. **requests**: Used in the CLI tool for fetching HTML content from URLs.

### Development Technologies

1. **Poetry**: Used for dependency management and packaging. Poetry is the primary tool for managing dependencies, building, and publishing the package.
2. **pytest**: Used for testing.
3. **Black**: Used for code formatting.
4. **Ruff/Flake8**: Used for linting.
5. **mypy**: Used for static type checking.
6. **tox**: Used for testing across multiple Python versions.

## Development Setup

### Environment Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/username/python-readability.git
   cd python-readability
   ```

2. **Install Poetry**:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. **Install dependencies**:
   ```bash
   poetry install
   ```

4. **Activate the virtual environment**:
   ```bash
   poetry shell
   ```

### Project Structure

```
python-readability/
├── readability/
│   ├── __init__.py
│   ├── models.py
│   ├── parser.py
│   ├── regexps.py
│   └── utils.py
├── cli/
│   ├── __init__.py
│   └── main.py
├── scripts/
│   └── publish.py
├── tests/
│   ├── conftest.py
│   ├── test_readability.py
│   ├── test_categories.py
│   ├── debug_tools.py
│   ├── scripts/
│   │   ├── verify_test_cases.py
│   │   ├── test-case-migration-script.py
│   │   └── enhance_comparison_functions.py
│   ├── docs/
│   │   ├── test-improvement-plan.md
│   │   └── ...
│   └── test-pages/
│       ├── 001/
│       │   ├── source.html
│       │   ├── expected.html
│       │   └── expected-metadata.json
│       └── ...
├── pyproject.toml
├── README.md
├── CONTRIBUTING.md
├── PACKAGING.md
└── LICENSE
```

### Development Workflow

1. **Run tests**:
   ```bash
   poetry run pytest
   ```

2. **Format code**:
   ```bash
   poetry run black readability tests
   ```

3. **Lint code**:
   ```bash
   poetry run ruff readability tests
   ```

4. **Type check**:
   ```bash
   poetry run mypy readability
   ```

5. **Build package**:
   ```bash
   poetry build
   ```

6. **Publish package**:
   ```bash
   python scripts/publish.py
   ```

## Technical Constraints

### Python Version Compatibility

The library is designed to be compatible with Python 3.8 and above. This ensures broad compatibility while still allowing the use of modern Python features like f-strings, type hints, dataclasses, and other features introduced in Python 3.8 such as the walrus operator (:=) and more precise typing features.

### Performance Considerations

While Python is generally slower than Go, we aim to optimize the library for performance where possible:

1. **Use lxml parser**: The lxml parser is significantly faster than the default HTML parser in BeautifulSoup.
2. **Minimize DOM traversal**: DOM traversal is expensive, so we minimize it where possible.
3. **Use compiled regular expressions**: We compile regular expressions once and reuse them.
4. **Avoid unnecessary string operations**: String operations can be expensive, so we minimize them.

### Memory Usage

The library is designed to be memory-efficient:

1. **Stream processing**: Where possible, we process HTML in a streaming fashion to avoid loading the entire document into memory.
2. **Garbage collection**: We explicitly remove references to large objects when they are no longer needed.
3. **Avoid unnecessary copies**: We avoid making unnecessary copies of large strings or DOM trees.

## Dependencies

### Runtime Dependencies

| Dependency | Version | Purpose |
|------------|---------|---------|
| beautifulsoup4 | >=4.9.0 | HTML parsing and DOM manipulation |
| lxml | >=4.5.0 | HTML parser backend for BeautifulSoup |
| python-dateutil | >=2.8.0 | Date parsing for metadata extraction |
| requests | >=2.23.0 | HTTP requests for CLI tool |

### Development Dependencies

| Dependency | Version | Purpose |
|------------|---------|---------|
| pytest | >=6.0.0 | Testing |
| black | >=20.8b1 | Code formatting |
| ruff | >=0.0.1 | Linting |
| mypy | >=0.800 | Static type checking |
| tox | >=3.20.0 | Testing across multiple Python versions |

## API Design

### Public API

The public API is designed to be simple and intuitive:

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
    print(f"Content: {article.content}")
```

### Error Handling

Following the Go implementation's pattern, we use explicit error returns rather than exceptions for the main API. This makes the API more predictable and easier to use, especially for users coming from Go.

```python
article, error = parser.parse(html_content, url=url)
if error:
    # Handle error
```

### Configuration

The library provides configuration options through the `Readability` class:

```python
parser = Readability(
    min_text_length=25,
    retry=True,
    url_rewriting=True,
    debug=False
)
```

## Compatibility with Go Implementation

### API Compatibility

The Python API is designed to be similar to the Go API where it makes sense, but adapted to be more Pythonic. The main differences are:

1. **Method naming**: We use snake_case for method names instead of camelCase.
2. **Configuration**: We use a more Pythonic configuration approach with keyword arguments.
3. **Error handling**: We use explicit error returns, but in a more Pythonic way.

### Behavior Compatibility

The behavior of the Python implementation should match the Go implementation as closely as possible:

1. **Content extraction**: The same content should be extracted from the same HTML.
2. **Metadata extraction**: The same metadata should be extracted from the same HTML.
3. **Error handling**: The same errors should be returned in the same situations.

### Test Compatibility

The test suite is designed to ensure compatibility with the Go implementation:

1. **Test cases**: We use the same test cases as the Go implementation.
2. **Expected output**: We compare the output of the Python implementation with the expected output from the Go implementation.
3. **Edge cases**: We test the same edge cases as the Go implementation.
