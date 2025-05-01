# Packaging Guide for Readability Python

This document provides instructions for building and publishing the Python Readability package to PyPI.

## Prerequisites

Make sure you have the following tools installed:

- Poetry: `pip install poetry`
- Build (optional): `pip install build`

## Building the Package

```bash
# Build the package
poetry build
```

This will create both source distribution (`.tar.gz`) and wheel (`.whl`) files in the `dist/` directory.

## Testing the Package Locally

Before publishing, you can test the package locally:

```bash
# Install the package in development mode
poetry install

# Or install the built package
pip install dist/readability_python-0.3.0-py3-none-any.whl
```

## Publishing to PyPI

### Using the Publish Script

We provide a convenient script for building and publishing the package:

```bash
# Publish to TestPyPI (recommended for testing)
python scripts/publish.py --test

# Publish to PyPI
python scripts/publish.py

# Clean build artifacts before building
python scripts/publish.py --clean
```

### Using Poetry Manually

```bash
# Publish to PyPI
poetry publish

# Publish to TestPyPI
poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry publish --repository testpypi
```

## PyPI Credentials

Before publishing, make sure you have your PyPI credentials set up:

```bash
poetry config pypi-token.pypi <your-pypi-token>
poetry config pypi-token.testpypi <your-testpypi-token>
```

## Version Management

When releasing a new version:

1. Update the version in `pyproject.toml`
2. Update the version in `readability/__init__.py`
3. Commit the changes
4. Tag the commit with the version number: `git tag v0.3.0`
5. Push the tag: `git push origin v0.3.0`
6. Build and publish the package

## Installation from PyPI

Once published, users can install the package with:

```bash
pip install readability-python
```

Or from TestPyPI:

```bash
pip install --index-url https://test.pypi.org/simple/ readability-python
```
