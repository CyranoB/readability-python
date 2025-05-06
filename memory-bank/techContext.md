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
3. **pytest-xdist**: Used for parallel test execution to improve test performance.
4. **pytest-mock**: Used for mocking dependencies in tests.
5. **pytest-cov**: Used for code coverage reporting.
6. **Black**: Used for code formatting.
7. **Ruff/Flake8**: Used for linting.
8. **mypy**: Used for static type checking.
9. **tox**: Used for testing across multiple Python versions.
10. **SonarQube/SonarCloud**: Used for code quality analysis and continuous inspection.

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
│   ├── errors.py
│   └── main.py
├── scripts/
│   ├── publish.py
│   ├── coverage.py
│   └── run_tests.py
├── tests/
│   ├── conftest.py
│   ├── helpers.py
│   ├── test_readability.py
│   ├── test_categories.py
│   ├── test_html_parsing.py
│   ├── test_metadata_extraction.py
│   ├── test_content_identification.py
│   ├── test_content_cleaning.py
│   ├── test_url_handling.py
│   ├── test_visibility_detection.py
│   ├── test_text_normalization.py
│   ├── test_real_world.py
│   ├── test_utils.py
│   ├── test_errors.py
│   ├── test_cli.py
│   ├── test_regexps.py
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
├── coverage-reports/
│   └── coverage.xml
├── test-reports/
│   └── test-results.xml
├── pyproject.toml
├── pytest.ini
├── .coveragerc
├── sonar-project.properties
├── README.md
├── CONTRIBUTING.md
├── PACKAGING.md
└── LICENSE
```

### Development Workflow

1. **Run tests**:
   ```bash
   # Run all tests
   poetry run pytest
   
   # Run tests by functional area
   poetry run python scripts/run_tests.py --html-parsing
   
   # Run tests using the comprehensive test file
   poetry run python scripts/run_tests.py --comprehensive
   
   # Run fast tests in parallel
   poetry run python scripts/run_tests.py --fast --parallel
   
   # Run tests without debug output
   poetry run python scripts/run_tests.py --all --no-debug
   
   # Run tests with coverage report
   poetry run python scripts/coverage.py
   
   # Generate HTML coverage report
   poetry run python scripts/coverage.py --html
   
   # Generate XML coverage report for SonarQube
   poetry run python scripts/coverage.py --xml --fix-paths
   
   # Generate JUnit XML test results
   poetry run python scripts/coverage.py --junit
   
   # Run tests with all reports in a single run
   poetry run python scripts/coverage.py --all --parallel --jobs 4 --split-tests --fix-paths
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
| pytest-xdist | >=2.5.0 | Parallel test execution |
| pytest-cov | >=2.12.0 | Code coverage reporting |
| pytest-mock | >=3.6.0 | Mocking dependencies in tests |
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

### Test Infrastructure

### Test Organization

The test suite is organized by functional area to improve maintainability and execution speed:

1. **Split Test Files**: Tests are split into separate files by functional area:
   - `test_html_parsing.py`: Tests for HTML parsing functionality
   - `test_metadata_extraction.py`: Tests for metadata extraction
   - `test_content_identification.py`: Tests for content identification
   - `test_content_cleaning.py`: Tests for content cleaning
   - `test_url_handling.py`: Tests for URL handling
   - `test_visibility_detection.py`: Tests for visibility detection
   - `test_text_normalization.py`: Tests for text normalization
   - `test_real_world.py`: Tests using real-world websites
   - `test_utils.py`: Tests for utility functions
   - `test_errors.py`: Tests for error handling
   - `test_cli.py`: Tests for the CLI
   - `test_regexps.py`: Tests for regular expressions

2. **Comprehensive Test File**: The `test_readability.py` file serves as a comprehensive test runner that includes all tests.

3. **Test Categorization**: Tests are categorized by functional area, criticality level, and test type using pytest marks.

### Test Execution

The test suite can be executed in various ways:

1. **Parallel Execution**: Tests can be run in parallel using pytest-xdist to improve execution speed.
2. **Test Subsetting**: Tests can be run by functional area, criticality level, or test type.
3. **Debug Output Control**: Debug output generation can be disabled to improve test execution speed.

### Test Reporting

The test suite supports various reporting formats:

1. **Terminal Report**: Basic test results are displayed in the terminal.
2. **HTML Report**: A detailed HTML report can be generated for human-readable analysis.
3. **XML Report**: An XML report can be generated for integration with CI/CD tools.
4. **JUnit XML Report**: A JUnit XML report can be generated for integration with CI/CD tools.

### CI/CD Integration

The test suite is integrated with CI/CD tools:

1. **GitHub Actions**: The test suite is run on GitHub Actions for continuous integration.
2. **SonarQube/SonarCloud**: Code quality analysis is performed using SonarQube/SonarCloud.
3. **Coverage Reports**: Coverage reports are generated and uploaded to SonarQube/SonarCloud.
4. **Test Results**: Test results are generated and uploaded to GitHub Actions.

## Test Compatibility

The test suite is designed to ensure compatibility with the Go implementation:

1. **Test Cases**: We use the same test cases as the Go implementation.
2. **Expected Output**: We compare the output of the Python implementation with the expected output from the Go implementation.
3. **Edge Cases**: We test the same edge cases as the Go implementation.
4. **Real-world Websites**: We test the library with real-world websites to ensure it works in practice.
