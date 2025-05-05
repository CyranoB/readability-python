#!/usr/bin/env python
"""Script to run targeted test subsets for readability-python."""

import argparse
import os
import subprocess
import sys
from enum import Enum


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


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="Run targeted test subsets")
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--all", action="store_true", help="Run all tests")
    group.add_argument("--fast", action="store_true", help="Run only fast tests (excludes real-world tests)")
    group.add_argument("--slow", action="store_true", help="Run only slow tests (only real-world tests)")
    
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
    if args.all:
        # Run all tests (no marker filtering)
        pass
    elif args.fast:
        markers = [f"area_{area.name.lower()}" for area in FAST_AREAS]
        cmd.append(f"-m \"{' or '.join(markers)}\"")
    elif args.slow:
        markers = [f"area_{area.name.lower()}" for area in SLOW_AREAS]
        cmd.append(f"-m \"{' or '.join(markers)}\"")
    else:
        # Individual area
        for area in FunctionalArea:
            flag_name = f"{area.name.lower().replace('_', '-')}"
            if getattr(args, flag_name.replace("-", "_"), False):
                cmd.append(f"-m area_{area.name.lower()}")
                break
    
    # Add the test file
    cmd.append("tests/test_readability.py")
    
    # Print command for transparency
    print(f"Running: {' '.join(cmd)}")
    
    # Execute the command
    return subprocess.call(" ".join(cmd), shell=True)


if __name__ == "__main__":
    sys.exit(main())
