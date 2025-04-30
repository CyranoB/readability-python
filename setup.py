#!/usr/bin/env python3
"""Setup script for python-readability."""

from setuptools import setup, find_packages

# Read version from readability/__init__.py
with open("readability/__init__.py", "r") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip('"\'')
            break
    else:
        version = "0.1.0"

# Read long description from README.md
with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="python-readability",
    version=version,
    description="Python port of the go-readability library for extracting the main content from web pages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Python Readability Team",
    author_email="python-readability@example.com",
    url="https://github.com/python-readability/python-readability",
    packages=find_packages(include=["readability", "readability.*", "cli", "cli.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup :: HTML"
    ],
    keywords="readability, html, content-extraction, web-scraping, mozilla",
    python_requires=">=3.8",
    install_requires=[
        "beautifulsoup4>=4.12.0",
        "lxml>=4.9.0",
        "python-dateutil>=2.8.2",
        "requests>=2.28.0",
    ],
    entry_points={
        "console_scripts": [
            "python-readability=cli.main:main",
        ],
    },
)
