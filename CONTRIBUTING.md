# Contributing to Python Readability

Thank you for your interest in contributing to Python Readability! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

Please be respectful and considerate of others when contributing to this project. We aim to foster an inclusive and welcoming community.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/python-readability.git`
3. Create a branch for your changes: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Run tests to ensure your changes don't break existing functionality: `pytest`
6. Commit your changes: `git commit -m "Add your feature"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Create a pull request

## Development Environment

### Requirements

- Python 3.6+
- Poetry (optional, for dependency management)

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/python-readability.git
cd python-readability

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

## Code Style

We follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide for Python code. Additionally:

- Use [Black](https://black.readthedocs.io/) for code formatting
- Use [Ruff](https://github.com/charliermarsh/ruff) or [Flake8](https://flake8.pycqa.org/) for linting
- Use [mypy](https://mypy.readthedocs.io/) for type checking
- Use docstrings for all public functions, classes, and methods
- Use type hints throughout the codebase

## Adding New Test Cases

The test suite is organized by functional area, criticality level, and test type. When adding new test cases, follow these steps:

1. Create a new directory in `tests/test-pages/` with a descriptive name
2. Add the following files to the directory:
   - `source.html` - The HTML to parse
   - `expected.html` - The expected content
   - `expected-metadata.json` - The expected metadata
3. Add the test case to `tests/test_categories.py` with appropriate categorization:

```python
# Example test case categorization
"your-test-case": (FunctionalArea.CONTENT_CLEANING, Criticality.P1, TestType.FEATURE, 
                  "Description of your test case"),
```

### Test Case Categories

#### Functional Areas
- HTML_PARSING: Tests for HTML parsing functionality
- METADATA_EXTRACTION: Tests for metadata extraction
- CONTENT_IDENTIFICATION: Tests for identifying the main content
- CONTENT_CLEANING: Tests for cleaning the extracted content
- URL_HANDLING: Tests for URL handling and conversion
- VISIBILITY_DETECTION: Tests for detecting and handling hidden elements
- TEXT_NORMALIZATION: Tests for text normalization
- REAL_WORLD: Tests using real-world websites

#### Criticality Levels
- P0: Critical functionality that must work
- P1: High-priority functionality with significant impact
- P2: Medium-priority functionality that should work but has workarounds
- P3: Low-priority functionality with minimal impact

#### Test Types
- BASIC: Tests for basic functionality
- FEATURE: Tests for specific features
- EDGE_CASE: Tests for handling edge cases
- REAL_WORLD: Tests using real-world websites

## Pull Request Process

1. Ensure your code follows the code style guidelines
2. Update the documentation if necessary
3. Add tests for new functionality
4. Ensure all tests pass
5. Update the README.md if necessary
6. Submit a pull request with a clear description of the changes

## Reporting Issues

If you find a bug or have a feature request, please create an issue on the GitHub repository. Please include:

- A clear and descriptive title
- A detailed description of the issue or feature request
- Steps to reproduce the issue (if applicable)
- Expected behavior
- Actual behavior
- Screenshots (if applicable)
- Environment information (OS, Python version, etc.)

## License

By contributing to this project, you agree that your contributions will be licensed under the project's MIT License.
