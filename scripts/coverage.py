#!/usr/bin/env python3
"""
Script to run code coverage reports for the readability-python project.

Usage:
    python scripts/coverage.py [--html] [--xml] [--report] [--junit] [--all] [--min-coverage PERCENTAGE] [--parallel] [--jobs JOBS] [--split-tests] [--fix-paths]

Options:
    --html          Generate HTML coverage report in the coverage_html directory
    --xml           Generate XML coverage report (for CI tools)
    --report        Show coverage report in the terminal (default if no other options specified)
    --junit         Generate JUnit XML test results (for CI tools)
    --junit-output  Path for JUnit XML output (default: test-reports/test-results.xml)
    --all           Generate all report formats (HTML, XML, terminal, and JUnit)
    --min-coverage  Set minimum required coverage percentage (e.g., --min-coverage 80)
    --parallel, -p  Run tests in parallel (RECOMMENDED for faster test execution)
    --jobs, -j      Number of parallel jobs (default: auto)
    --split-tests   Use split test files instead of default discovery (faster)
    --fix-paths     Fix paths in coverage reports for SonarQube

Note:
    Always use the --parallel and --split-tests flags for faster test execution, especially on multi-core systems.
    For example: python scripts/coverage.py --all --parallel --jobs 4 --split-tests
"""

import os
import sys
import subprocess
import argparse
import re
from pathlib import Path


# Map functional areas to their corresponding test files
SPLIT_TEST_FILES = [
    "tests/test_html_parsing.py",
    "tests/test_metadata_extraction.py",
    "tests/test_content_identification.py",
    "tests/test_content_cleaning.py",
    "tests/test_url_handling.py",
    "tests/test_visibility_detection.py",
    "tests/test_text_normalization.py",
    "tests/test_real_world.py",
    "tests/test_utils.py",
    "tests/test_errors.py",
    "tests/test_cli.py",
    "tests/test_regexps.py"
]


def run_coverage(html=False, xml=False, report=True, junit=False, junit_output=None,
                min_coverage=None, parallel=False, jobs=None, split_tests=False, fix_paths=False):
    """Run pytest with coverage options."""
    cmd = ["python", "-m", "pytest", "--cov=readability", "--cov=cli"]
    
    # Add parallel execution options
    if parallel:
        if jobs:
            cmd.extend(["-n", str(jobs)])
        else:
            cmd.extend(["-n", "auto"])
    
    # Ensure the coverage-reports directory exists
    if xml:
        os.makedirs("coverage-reports", exist_ok=True)
    
    # Ensure the test-reports directory exists
    if junit:
        os.makedirs(os.path.dirname(junit_output or "test-reports/test-results.xml"), exist_ok=True)
    
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
    
    # Add JUnit XML output
    if junit:
        cmd.append(f"--junitxml={junit_output or 'test-reports/test-results.xml'}")
    
    # Add minimum coverage requirement
    if min_coverage is not None:
        cmd.append(f"--cov-fail-under={min_coverage}")
    
    # Add split test files if requested
    if split_tests:
        cmd.extend(SPLIT_TEST_FILES)
    
    # Run the command
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    
    # Fix paths in coverage report if requested
    if fix_paths and xml:
        fix_coverage_paths("coverage-reports/coverage.xml")
    
    return result.returncode


def fix_coverage_paths(coverage_file):
    """Fix paths in coverage report for SonarQube.
    
    Args:
        coverage_file: Path to the coverage XML file
    """
    print(f"Fixing paths in {coverage_file}...")
    
    # Read the coverage file
    with open(coverage_file, "r") as f:
        content = f.read()
    
    # Replace all absolute paths in source tags with relative path
    content = re.sub(r'<sources>.*?</sources>', '<sources><source>.</source></sources>', content, flags=re.DOTALL)
    
    # Add module prefixes to filenames for cli module
    content = re.sub(r'<class name="(errors|main)\.py" filename="\1\.py"', 
                    r'<class name="\1.py" filename="cli/\1.py"', content)
    
    # Add module prefixes to filenames for readability module
    content = re.sub(r'<class name="(models|parser|regexps|utils)\.py" filename="\1\.py"', 
                    r'<class name="\1.py" filename="readability/\1.py"', content)
    
    # Write the fixed content back
    with open(coverage_file, "w") as f:
        f.write(content)
    
    print(f"Fixed paths in {coverage_file}")


def main():
    """Parse arguments and run coverage."""
    parser = argparse.ArgumentParser(description="Run code coverage for readability-python")
    parser.add_argument("--html", action="store_true", help="Generate HTML report")
    parser.add_argument("--xml", action="store_true", help="Generate XML report")
    parser.add_argument("--report", action="store_true", help="Show terminal report")
    parser.add_argument("--junit", action="store_true", help="Generate JUnit XML test results")
    parser.add_argument("--junit-output", help="Path for JUnit XML output (default: test-reports/test-results.xml)")
    parser.add_argument("--all", action="store_true", 
                       help="Generate all report formats (HTML, XML, terminal, and JUnit)")
    parser.add_argument("--min-coverage", type=float, help="Minimum coverage percentage")
    parser.add_argument("--parallel", "-p", action="store_true", help="Run tests in parallel")
    parser.add_argument("--jobs", "-j", type=int, help="Number of parallel jobs (default: auto)")
    parser.add_argument("--split-tests", action="store_true", 
                       help="Use split test files instead of default discovery (faster)")
    parser.add_argument("--fix-paths", action="store_true", 
                       help="Fix paths in coverage reports for SonarQube")
    
    args = parser.parse_args()
    
    # Handle --all flag that generates all report types
    if args.all:
        args.html = True
        args.xml = True
        args.report = True
        args.junit = True
    # Default to terminal report if no options specified
    elif not (args.html or args.xml or args.report or args.junit):
        args.report = True
    
    return run_coverage(
        html=args.html,
        xml=args.xml,
        report=args.report,
        junit=args.junit,
        junit_output=args.junit_output,
        min_coverage=args.min_coverage,
        parallel=args.parallel,
        jobs=args.jobs,
        split_tests=args.split_tests,
        fix_paths=args.fix_paths
    )


if __name__ == "__main__":
    sys.exit(main())
