#!/usr/bin/env python3
"""
Script to build and publish the python-readability package to PyPI.

Usage:
    python scripts/publish.py [--test]

Options:
    --test: Upload to TestPyPI instead of PyPI
"""

import os
import sys
import subprocess
import argparse


def run_command(command, check=True):
    """Run a shell command and print its output."""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, check=check, text=True)
    return result


def build_package():
    """Build the package using Poetry."""
    print("\n=== Building package ===")
    run_command("poetry build")


def build_package_setuptools():
    """Build the package using setuptools."""
    print("\n=== Building package with setuptools ===")
    run_command("python setup.py sdist bdist_wheel")


def publish_package(test=False):
    """Publish the package to PyPI or TestPyPI."""
    if test:
        print("\n=== Publishing to TestPyPI ===")
        run_command("poetry config repositories.testpypi https://test.pypi.org/legacy/")
        run_command("poetry publish --repository testpypi")
    else:
        print("\n=== Publishing to PyPI ===")
        run_command("poetry publish")


def publish_package_twine(test=False):
    """Publish the package to PyPI or TestPyPI using twine."""
    if test:
        print("\n=== Publishing to TestPyPI with twine ===")
        run_command("twine upload --repository-url https://test.pypi.org/legacy/ dist/*")
    else:
        print("\n=== Publishing to PyPI with twine ===")
        run_command("twine upload dist/*")


def clean_build_artifacts():
    """Clean up build artifacts."""
    print("\n=== Cleaning build artifacts ===")
    run_command("rm -rf build/ dist/ *.egg-info/")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Build and publish python-readability to PyPI")
    parser.add_argument("--test", action="store_true", help="Upload to TestPyPI instead of PyPI")
    parser.add_argument("--setuptools", action="store_true", help="Use setuptools instead of Poetry")
    parser.add_argument("--clean", action="store_true", help="Clean build artifacts before building")
    args = parser.parse_args()

    # Change to the project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_root)
    
    # Clean build artifacts if requested
    if args.clean:
        clean_build_artifacts()
    
    # Build the package
    if args.setuptools:
        build_package_setuptools()
    else:
        build_package()
    
    # Ask for confirmation before publishing
    if args.test:
        target = "TestPyPI"
    else:
        target = "PyPI"
    
    confirm = input(f"\nDo you want to publish to {target}? [y/N] ")
    if confirm.lower() != "y":
        print("Aborted.")
        return
    
    # Publish the package
    if args.setuptools:
        publish_package_twine(args.test)
    else:
        publish_package(args.test)
    
    print("\nDone!")


if __name__ == "__main__":
    main()
