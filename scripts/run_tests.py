#!/usr/bin/env python
"""
Script to run targeted test subsets for readability-python.

This script allows running specific subsets of tests based on functional areas,
performance categories, or using the split test files for better parallelization.

Usage:
    python scripts/run_tests.py --all [--parallel] [--jobs N] [--no-debug]
    python scripts/run_tests.py --fast [--parallel] [--jobs N] [--no-debug]
    python scripts/run_tests.py --slow [--parallel] [--jobs N] [--no-debug]
    python scripts/run_tests.py --html-parsing [--parallel] [--jobs N] [--no-debug]
    python scripts/run_tests.py --comprehensive [--parallel] [--jobs N] [--no-debug]

Options:
    --all            Run all tests using split test files
    --fast           Run only fast tests (excludes real-world tests)
    --slow           Run only slow tests (only real-world tests)
    --comprehensive  Run all tests using the comprehensive test file (test_readability.py)
    --parallel, -p   Run tests in parallel
    --jobs, -j       Number of parallel jobs (default: auto)
    --no-debug       Disable debug output generation
    --verbose, -v    Enable verbose output
"""

import argparse
import os
import subprocess
import sys
from enum import Enum
from pathlib import Path


class FunctionalArea(Enum):
    """Functional areas for test categorization."""
    HTML_PARSING = "HTML Parsing"
    METADATA_EXTRACTION = "Metadata Extraction"
    CONTENT_IDENTIFICATION = "Content Identification"
    CONTENT_CLEANING = "Content Cleaning"
    URL_HANDLING = "URL Handling"
    VISIBILITY_DETECTION = "Visibility Detection"
    TEXT_NORMALIZATION = "Text Normalization"
    REAL_WORLD = "Real-world Websites"


# Map functional areas to their corresponding test files
AREA_TO_TEST_FILE = {
    FunctionalArea.HTML_PARSING: "tests/test_html_parsing.py",
    FunctionalArea.METADATA_EXTRACTION: "tests/test_metadata_extraction.py",
    FunctionalArea.CONTENT_IDENTIFICATION: "tests/test_content_identification.py",
    FunctionalArea.CONTENT_CLEANING: "tests/test_content_cleaning.py",
    FunctionalArea.URL_HANDLING: "tests/test_url_handling.py",
    FunctionalArea.VISIBILITY_DETECTION: "tests/test_visibility_detection.py",
    FunctionalArea.TEXT_NORMALIZATION: "tests/test_text_normalization.py",
    FunctionalArea.REAL_WORLD: "tests/test_real_world.py",
}

# Comprehensive test file that contains all tests
COMPREHENSIVE_TEST_FILE = "tests/test_readability.py"


# Group areas into performance categories
FAST_AREAS = [
    FunctionalArea.HTML_PARSING,
    FunctionalArea.METADATA_EXTRACTION,
    FunctionalArea.CONTENT_IDENTIFICATION,
    FunctionalArea.CONTENT_CLEANING, 
    FunctionalArea.URL_HANDLING,
    FunctionalArea.VISIBILITY_DETECTION,
    FunctionalArea.TEXT_NORMALIZATION
]

SLOW_AREAS = [
    FunctionalArea.REAL_WORLD
]

# Get test files for a list of areas
def get_test_files_for_areas(areas):
    """Get test files for a list of functional areas.
    
    Args:
        areas: List of FunctionalArea enum values
        
    Returns:
        List of test file paths
    """
    return [AREA_TO_TEST_FILE[area] for area in areas]


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="Run targeted test subsets")
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--all", action="store_true", help="Run all tests using split test files")
    group.add_argument("--fast", action="store_true", help="Run only fast tests (excludes real-world tests)")
    group.add_argument("--slow", action="store_true", help="Run only slow tests (only real-world tests)")
    group.add_argument("--comprehensive", action="store_true", 
                      help="Run all tests using the comprehensive test file (test_readability.py)")
    
    for area in FunctionalArea:
        flag = f"--{area.name.lower().replace('_', '-')}"
        group.add_argument(
            flag, action="store_true", 
            help=f"Run only {area.value} tests"
        )
    
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    parser.add_argument("--parallel", "-p", action="store_true", help="Run tests in parallel")
    parser.add_argument("--jobs", "-j", type=int, help="Number of parallel jobs (default: auto)")
    parser.add_argument("--no-debug", action="store_true", help="Disable debug output generation")
    
    args = parser.parse_args()
    
    # Build the pytest command
    cmd = ["pytest"]
    
    if args.verbose:
        cmd.append("-v")
    
    if args.parallel:
        if args.jobs:
            cmd.extend(["-n", str(args.jobs)])
        else:
            cmd.extend(["-n", "auto"])
    
    if args.no_debug:
        # Set environment variable to disable debug output
        os.environ["DISABLE_DEBUG_OUTPUT"] = "1"
    
    # Determine which tests to run
    test_files = []
    
    if args.comprehensive:
        # Use the comprehensive test file
        test_files = [COMPREHENSIVE_TEST_FILE]
    elif args.all:
        # Run all tests using split test files
        test_files = list(AREA_TO_TEST_FILE.values())
    elif args.fast:
        # Run fast tests using split test files
        test_files = get_test_files_for_areas(FAST_AREAS)
    elif args.slow:
        # Run slow tests using split test files
        test_files = get_test_files_for_areas(SLOW_AREAS)
    else:
        # Individual area
        for area in FunctionalArea:
            flag_name = f"{area.name.lower().replace('_', '-')}"
            if getattr(args, flag_name.replace("-", "_"), False):
                test_files = [AREA_TO_TEST_FILE[area]]
                break
    
    # Add the test files to the command
    cmd.extend(test_files)
    
    # Print command for transparency
    print(f"Running: {' '.join(cmd)}")
    
    # Execute the command
    return subprocess.call(" ".join(cmd), shell=True)


if __name__ == "__main__":
    sys.exit(main())
