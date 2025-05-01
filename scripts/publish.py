#!/usr/bin/env python3
"""
Script to build and publish the readability-python package to PyPI.

Usage:
    python scripts/publish.py [--test] [--clean]

Options:
    --test: Upload to TestPyPI instead of PyPI
    --clean: Clean build artifacts before building
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


def publish_package(test=False):
    """Publish the package to PyPI or TestPyPI."""
    if test:
        print("\n=== Publishing to TestPyPI ===")
        run_command("poetry config repositories.testpypi https://test.pypi.org/legacy/")
        run_command("poetry publish --repository testpypi")
    else:
        print("\n=== Publishing to PyPI ===")
        run_command("poetry publish")


def clean_build_artifacts():
    """Clean up build artifacts."""
    print("\n=== Cleaning build artifacts ===")
    run_command("rm -rf build/ dist/ *.egg-info/")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Build and publish readability-python to PyPI")
    parser.add_argument("--test", action="store_true", help="Upload to TestPyPI instead of PyPI")
    parser.add_argument("--clean", action="store_true", help="Clean build artifacts before building")
    args = parser.parse_args()

    # Change to the project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_root)
    
    # Clean build artifacts if requested
    if args.clean:
        clean_build_artifacts()
    
    # Build the package
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
    publish_package(args.test)
    
    print("\nDone!")


if __name__ == "__main__":
    main()
