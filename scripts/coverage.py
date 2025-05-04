#!/usr/bin/env python3
"""
Script to run code coverage reports for the readability-python project.

Usage:
    python scripts/coverage.py [--html] [--xml] [--report] [--min-coverage PERCENTAGE]

Options:
    --html          Generate HTML coverage report in the coverage_html directory
    --xml           Generate XML coverage report (for CI tools)
    --report        Show coverage report in the terminal (default if no other options specified)
    --min-coverage  Set minimum required coverage percentage (e.g., --min-coverage 80)
"""

import sys
import subprocess
import argparse


def run_coverage(html=False, xml=False, report=True, min_coverage=None):
    """Run pytest with coverage options."""
    cmd = ["python", "-m", "pytest", "--cov=readability", "--cov=cli"]
    
    # Add report formats
    if html:
        cmd.append("--cov-report=html")
    if xml:
        cmd.append("--cov-report=xml")
    if report:
        cmd.append("--cov-report=term")
    elif not html and not xml:
        # If no report format is specified, default to terminal
        cmd.append("--cov-report=term")
    
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
    parser.add_argument("--min-coverage", type=float, help="Minimum coverage percentage")
    
    args = parser.parse_args()
    
    # Default to terminal report if no options specified
    if not (args.html or args.xml or args.report):
        args.report = True
    
    return run_coverage(
        html=args.html,
        xml=args.xml,
        report=args.report,
        min_coverage=args.min_coverage
    )


if __name__ == "__main__":
    sys.exit(main())
