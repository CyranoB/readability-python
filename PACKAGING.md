# Packaging Guide for Readability Python

This document provides instructions for building and publishing the Python Readability package to PyPI.

## Prerequisites

Make sure you have the following tools installed:

- Poetry (recommended): `pip install poetry`
- Setuptools and wheel: `pip install setuptools wheel`
- Twine (for uploading to PyPI): `pip install twine`
- Build: `pip install build`

## Building the Package

### Using Poetry (Recommended)

```bash
# Build the package
poetry build
```

This will create both source distribution (`.tar.gz`) and wheel (`.whl`) files in the `dist/` directory.

### Using Setuptools

```bash
# Build the package
python setup.py sdist bdist_wheel
```

This will also create both source distribution and wheel files in the `dist/` directory.

## Testing the Package Locally

Before publishing, you can test the package locally:

```bash
# Install the package in development mode
pip install -e .

# Or install the built package
pip install dist/readability_python-0.1.0-py3-none-any.whl
```

## Publishing to PyPI

### Using the Publish Script

We provide a convenient script for building and publishing the package:

```bash
# Publish to TestPyPI (recommended for testing)
python scripts/publish.py --test

# Publish to PyPI
python scripts/publish.py

# Use setuptools instead of Poetry
python scripts/publish.py --setuptools

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

### Using Twine Manually

```bash
# Publish to PyPI
twine upload dist/*

# Publish to TestPyPI
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

## PyPI Credentials

Before publishing, make sure you have your PyPI credentials set up:

### For Poetry

```bash
poetry config pypi-token.pypi <your-pypi-token>
poetry config pypi-token.testpypi <your-testpypi-token>
```

### For Twine

Create or edit `~/.pypirc`:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = <your-pypi-token>

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = <your-testpypi-token>
```

## Version Management

When releasing a new version:

1. Update the version in `pyproject.toml`
2. Update the version in `readability/__init__.py`
3. Commit the changes
4. Tag the commit with the version number: `git tag v0.1.0`
5. Push the tag: `git push origin v0.1.0`
6. Build and publish the package

## Installation from PyPI

Once published, users can install the package with:

```bash
pip install readability-python
```

Or from TestPyPI:

```bash
pip install --index-url https://test.pypi.org/simple/ readability-python
