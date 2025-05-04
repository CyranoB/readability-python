#!/usr/bin/env python3
"""
Script to run code coverage reports for the readability-python project.

Usage:
    python scripts/coverage.py [--html] [--xml] [--report] [--all] [--min-coverage PERCENTAGE]

Options:
    --html          Generate HTML coverage report in the coverage_html directory
    --xml           Generate XML coverage report (for CI tools)
    --report        Show coverage report in the terminal (default if no other options specified)
    --all           Generate all report formats (HTML, XML, and terminal)
    --min-coverage  Set minimum required coverage percentage (e.g., --min-coverage 80)
"""

import os
import sys
import subprocess
import argparse


def run_coverage(html=False, xml=False, report=True, min_coverage=None):
    """Run pytest with coverage options."""
    cmd = ["python", "-m", "pytest", "--cov=readability", "--cov=cli"]
    
    # Ensure the coverage-reports directory exists
    if xml:
        os.makedirs("coverage-reports", exist_ok=True)
    
    # Build report formats list
    report_formats = []
    if html:
        report_formats.append("html")
    if xml:
        report_formats.append("xml:coverage-reports/coverage.xml")
    if report or not report_formats:
        report_formats.append("term")
    
    # Add report formats to command
    for fmt in report_formats:
        cmd.append(f"--cov-report={fmt}")
    
    # Add minimum coverage requirement
    if min_coverage is not None:
        cmd.append(f"--cov-fail-under={min_coverage}")
    
    # Run the command
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    return result.returncode


def main():
    """Parse arguments and run coverage."""
    parser = argparse.ArgumentParser(description="Run code coverage for readability-python")
    parser.add_argument("--html", action="store_true", help="Generate HTML report")
    parser.add_argument("--xml", action="store_true", help="Generate XML report")
    parser.add_argument("--report", action="store_true", help="Show terminal report")
    parser.add_argument("--all", action="store_true", help="Generate all report formats (HTML, XML, and terminal)")
    parser.add_argument("--min-coverage", type=float, help="Minimum coverage percentage")
    
    args = parser.parse_args()
    
    # Handle --all flag that generates all report types
    if args.all:
        args.html = True
        args.xml = True
        args.report = True
    # Default to terminal report if no options specified
    elif not (args.html or args.xml or args.report):
        args.report = True
    
    return run_coverage(
        html=args.html,
        xml=args.xml,
        report=args.report,
        min_coverage=args.min_coverage
    )


if __name__ == "__main__":
    sys.exit(main())
