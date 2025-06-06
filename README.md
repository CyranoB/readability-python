# Readability Python (v0.5.1)

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

The library includes a command-line interface for easy content extraction:

```bash
# Extract content from a URL
readability-python https://example.com/article --output article.html

# Extract content from a file
readability-python article.html --output extracted.html

# Output as JSON (includes all metadata)
readability-python https://example.com/article --format json --output article.json

# Output as plain text
readability-python https://example.com/article --format text --output article.txt

# Read from stdin
cat article.html | readability-python --output extracted.html

# Specify a custom user agent
readability-python https://example.com/article --user-agent "Mozilla/5.0 ..." --output article.html

# Set a custom timeout for HTTP requests
readability-python https://example.com/article --timeout 60 --output article.html

# Enable debug output
readability-python https://example.com/article --debug --output article.html
```

#### Error Handling

The CLI provides specific exit codes for different error types:

- `0`: Success
- `1`: Input error (file not found, invalid input)
- `2`: Network error (connection issues, timeout)
- `3`: Parsing error (HTML parsing failed)
- `4`: Output error (cannot write to output file)
- `10`: Unknown error

This allows for better scripting and automation when using the CLI in pipelines.

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

# Run tests with coverage report
python scripts/coverage.py

# Generate HTML coverage report
python scripts/coverage.py --html

# Generate XML report (for SonarQube/CI tools)
python scripts/coverage.py --xml

# Generate all report formats
python scripts/coverage.py --all

# Set minimum coverage requirement (fails if not met)
python scripts/coverage.py --min-coverage 70

# Generate JUnit XML test results (for CI tools)
python scripts/coverage.py --junit

# Specify JUnit XML output path
python scripts/coverage.py --junit --junit-output=test-reports/custom-results.xml

# Use split test files for better parallelization
python scripts/coverage.py --split-tests

# Fix paths in coverage reports for SonarQube
python scripts/coverage.py --fix-paths

# Combine options for CI/CD pipelines
python scripts/coverage.py --all --parallel --jobs 4 --split-tests --fix-paths --junit
```

### Running Test Subsets

To improve test execution speed, you can run specific subsets of tests using the `scripts/run_tests.py` script:

```bash
# Run only fast tests (excludes real-world website tests)
python scripts/run_tests.py --fast

# Run only real-world website tests (the slower ones)
python scripts/run_tests.py --slow

# Run tests for specific functional areas
python scripts/run_tests.py --html-parsing
python scripts/run_tests.py --metadata-extraction
python scripts/run_tests.py --content-identification
python scripts/run_tests.py --content-cleaning
python scripts/run_tests.py --url-handling
python scripts/run_tests.py --visibility-detection
python scripts/run_tests.py --text-normalization
python scripts/run_tests.py --real-world

# Run tests using the comprehensive test file (test_readability.py)
python scripts/run_tests.py --comprehensive

# Run tests in parallel (uses pytest-xdist)
python scripts/run_tests.py --fast --parallel

# Specify number of parallel jobs
python scripts/run_tests.py --all --parallel --jobs 4

# Run tests without generating debug output (faster)
python scripts/run_tests.py --all --no-debug

# Combine options for maximum speed
python scripts/run_tests.py --fast --parallel --no-debug
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

## SonarQube Integration

The project includes configuration for SonarQube/SonarCloud code quality analysis:

- Coverage reports are generated in the `coverage-reports` directory
- XML format coverage data is available for SonarQube analysis
- A `sonar-project.properties` file is included with recommended settings
- Path fixing is automatically applied to coverage reports for SonarQube compatibility

To run SonarQube analysis:

1. Generate coverage data with path fixing:
   ```bash
   python scripts/coverage.py --xml --fix-paths
   ```

2. Generate test results in JUnit format:
   ```bash
   python scripts/coverage.py --junit
   ```

3. Run the SonarQube scanner:
   ```bash
   sonar-scanner
   ```

For CI/CD pipelines, you can combine all steps into a single command:
```bash
python scripts/coverage.py --all --parallel --jobs 4 --split-tests --fix-paths --junit
```

This will generate all report formats, run tests in parallel, use split test files for better performance, fix paths for SonarQube, and generate JUnit XML test results.

## Comparison with Go Implementation

This library aims to be a high-fidelity port of the [go-readability](https://github.com/go-shiori/go-readability) library, with the following considerations:

- Maintains the same functionality and behavior
- Uses Python best practices and idioms where appropriate
- Adapts the API to be more Pythonic while maintaining the same core functionality
- Uses BeautifulSoup for HTML parsing instead of Go's DOM implementation
- Maps Go's DOM traversal methods to BeautifulSoup's methods

## Development

### Requirements

- Python 3.8+
- Poetry (recommended for dependency management)

### Setup

```bash
# Clone the repository
git clone https://github.com/CyranoB/readability-python.git
cd readability-python

# Install dependencies with Poetry (recommended)
poetry install

# Or with pip (alternative)
pip install -e ".[dev]"
```

### Development Workflow

```bash
# Run tests
poetry run pytest

# Format code
poetry run black readability tests

# Lint code
poetry run ruff readability tests

# Type check
poetry run mypy readability

# Build the package
poetry build

# Publish the package (requires PyPI credentials)
python scripts/publish.py
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

## New Features in v0.5.1

This release adds significant improvements to the test infrastructure for better CI/CD performance:

### Test Infrastructure Improvements
- **Split Test Files**: Updated `scripts/run_tests.py` to use functional area-specific test files
- **Comprehensive Mode**: Added `--comprehensive` flag to run tests using the original test file
- **JUnit XML Reports**: Added `--junit` option to generate JUnit XML test results
- **Path Fixing**: Added `--fix-paths` option to fix paths in coverage reports for SonarQube
- **Optimized CI Pipeline**: Reduced CI build time by ~60% by running tests only once

### Performance Improvements
- **Faster Test Execution**: Tests now run in parallel across multiple CPU cores
- **Better Resource Utilization**: More efficient use of system resources
- **Improved Maintainability**: Clearer organization of tests by functional area

## Previous Features in v0.5.0

The previous version added important improvements for handling character encoding issues:

### Encoding Support
- **Explicit encoding parameter**: Added `encoding` parameter to the `parse()` method to handle non-Latin character sets
- **Encoding detection**: Improved automatic encoding detection with validation
- **Encoding error handling**: Added detection and reporting of potential encoding issues
- **CLI encoding option**: Added `--encoding` / `-e` parameter to specify character encoding

### HTML Output Improvements
- **Proper HTML document structure**: Added complete HTML document structure to output
- **Encoding declaration**: Added UTF-8 charset meta tags to ensure correct rendering
- **Title preservation**: Article title is now included in the HTML output

### Other Improvements
- **Binary content handling**: Added support for reading binary content from files and stdin
- **Error reporting**: Enhanced error messages for encoding-related issues
- **Documentation**: Added comprehensive documentation for encoding handling

## Previous Improvements (v0.4.0)

The previous version included several improvements to enhance usability and maintainability:

### Test Infrastructure Improvements
- **Fixed test helper functions**: Renamed `test_individual_case` to `_test_individual_case` to prevent it from being collected as a standalone test
- **Fixed pytest warnings**: Added collection ignore for TestType class to eliminate warnings
- **Improved Git integration**: Untracked debug files from Git while preserving them on the filesystem
- **Enhanced test organization**: Better separation of test helper functions and actual test cases

### Enhanced CLI Features
- **Improved stdin handling**: Better detection of terminal input with user feedback
- **Chunk-based reading**: Efficiently handles large inputs by reading in chunks
- **Granular error handling**: Specific exit codes for different error types
- **Detailed error messages**: More informative error output for troubleshooting

### Code Quality Improvements
- **Extracted constants**: Replaced hardcoded values with named constants
- **Improved type hinting**: Added return type hints to internal methods
- **Better exception handling**: More specific exception handling for JSON parsing
- **Modern packaging**: Removed redundant setup.py in favor of Poetry-only approach

### Documentation Updates
- **Comprehensive CLI documentation**: Added examples for all CLI options
- **Error code documentation**: Documented exit codes for better scripting
- **Updated requirements**: Clarified Python version requirements
- **Improved development workflow**: Enhanced instructions for contributors

## License

This project is licensed under the Apache 2.0 License - see the LICENSE file for details.
