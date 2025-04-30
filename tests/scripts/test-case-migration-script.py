#!/usr/bin/env python3
"""
Test Case Migration Script for Python Readability

This script helps migrate missing test cases from the go-readability implementation
to the Python implementation.

Usage:
  python test-case-migration-script.py [--all] [--list] [case_name1 case_name2 ...]

Options:
  --all: Migrate all missing test cases
  --list: List missing test cases without migrating
  case_name1, case_name2, ...: Specific test cases to migrate
"""

import os
import sys
import shutil
from pathlib import Path
import argparse
import json

# Path definitions
# Adjust paths to be relative to the project root
PROJECT_ROOT = Path(__file__).parent.parent.parent
GO_TEST_DIR = PROJECT_ROOT / "go-readability/test-pages"
PYTHON_TEST_DIR = PROJECT_ROOT / "tests/test-pages"

# List of test cases to ignore (if they should not be migrated)
IGNORE_LIST = []

def list_test_cases(directory):
    """List all test case directories in the given directory."""
    if not directory.exists():
        print(f"Directory not found: {directory}")
        return []
        
    return [d for d in directory.iterdir() if d.is_dir()]

def get_missing_test_cases():
    """Identify test cases that exist in Go but not in Python implementation."""
    go_cases = set(d.name for d in list_test_cases(GO_TEST_DIR) if d.name not in IGNORE_LIST)
    python_cases = set(d.name for d in list_test_cases(PYTHON_TEST_DIR))
    
    return sorted(list(go_cases - python_cases))

def migrate_test_case(case_name):
    """Migrate a single test case from Go to Python implementation."""
    go_case_dir = GO_TEST_DIR / case_name
    python_case_dir = PYTHON_TEST_DIR / case_name
    
    if not go_case_dir.exists():
        print(f"Go test case not found: {go_case_dir}")
        return False
        
    if python_case_dir.exists():
        print(f"Python test case already exists: {python_case_dir}")
        return False
    
    # Create the Python test case directory
    python_case_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy the required files
    required_files = ["source.html", "expected.html", "expected-metadata.json"]
    for file_name in required_files:
        source_path = go_case_dir / file_name
        dest_path = python_case_dir / file_name
        
        # Skip if source doesn't exist
        if not source_path.exists():
            print(f"Warning: {file_name} not found in {go_case_dir}")
            continue
            
        # Copy the file
        shutil.copy2(source_path, dest_path)
        print(f"Copied: {source_path} -> {dest_path}")
    
    print(f"Successfully migrated test case: {case_name}")
    return True

def update_parameterized_tests(migrated_cases):
    """Update the parameterized test list in test_readability.py to include the migrated cases."""
    if not migrated_cases:
        return
        
    test_file_path = PROJECT_ROOT / "tests/test_readability.py"
    if not test_file_path.exists():
        print(f"Warning: Test file not found: {test_file_path}")
        print("Please manually update the parameterized test list.")
        return
    
    # Read the test file
    content = test_file_path.read_text(encoding="utf-8")
    
    # Find the parameterized test decorator
    import re
    pattern = r'@pytest\.mark\.parametrize\("case_name",\s*\[(.*?)\]\)'
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        print("Warning: Could not find parameterized test decorator.")
        print("Please manually update the parameterized test list.")
        print("Add the following test cases:")
        for case in migrated_cases:
            print(f'    "{case}",')
        return
    
    # Extract the existing test cases
    existing_cases_str = match.group(1)
    
    # Check if test cases are already in the list
    cases_to_add = []
    for case in migrated_cases:
        if f'"{case}"' not in existing_cases_str and f"'{case}'" not in existing_cases_str:
            cases_to_add.append(case)
    
    if not cases_to_add:
        print("All migrated test cases are already in the parameterized test list.")
        return
    
    # Add new cases to the end of the list
    new_cases_str = existing_cases_str
    if new_cases_str.strip().endswith(","):
        # If the last entry already has a comma, just add new entries
        for case in cases_to_add:
            new_cases_str += f'\n    "{case}",'
    else:
        # Add comma to the last entry and then add new entries
        new_cases_str += ","
        for case in cases_to_add:
            new_cases_str += f'\n    "{case}",'
    
    # Replace the old list with the new one
    new_content = content.replace(existing_cases_str, new_cases_str)
    
    # Write back to the file
    test_file_path.write_text(new_content, encoding="utf-8")
    
    print(f"Updated parameterized test list in {test_file_path}")
    print("Added test cases:")
    for case in cases_to_add:
        print(f'    "{case}"')

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Migrate test cases from Go to Python implementation")
    parser.add_argument("--all", action="store_true", help="Migrate all missing test cases")
    parser.add_argument("--list", action="store_true", help="List missing test cases without migrating")
    parser.add_argument("cases", nargs="*", help="Specific test cases to migrate")
    
    args = parser.parse_args()
    
    # Get missing test cases
    missing_cases = get_missing_test_cases()
    
    # List missing test cases if requested
    if args.list or (not args.all and not args.cases):
        print("Missing test cases:")
        for case in missing_cases:
            print(f"  {case}")
        return
    
    # Determine which test cases to migrate
    if args.all:
        cases_to_migrate = missing_cases
    elif args.cases:
        cases_to_migrate = [case for case in args.cases if case in missing_cases]
        
        # Check for invalid cases
        invalid_cases = [case for case in args.cases if case not in missing_cases]
        if invalid_cases:
            print("Warning: The following cases are not missing or do not exist:")
            for case in invalid_cases:
                print(f"  {case}")
    else:
        print("No test cases specified. Use --all to migrate all missing test cases.")
        return
    
    if not cases_to_migrate:
        print("No test cases to migrate.")
        return
    
    # Migrate the test cases
    print(f"Migrating {len(cases_to_migrate)} test cases...")
    migrated_cases = []
    for case in cases_to_migrate:
        if migrate_test_case(case):
            migrated_cases.append(case)
    
    # Update parameterized tests
    if migrated_cases:
        print(f"\nSuccessfully migrated {len(migrated_cases)} test cases.")
        update_parameterized_tests(migrated_cases)
    else:
        print("\nNo test cases were migrated.")

if __name__ == "__main__":
    main()
