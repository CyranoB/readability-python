#!/usr/bin/env python3
"""
Master script to prepare all necessary files for SonarQube analysis.
"""
import os
import sys
import subprocess

def run_command(cmd, description):
    """Run a command and print its output"""
    print(f"Running {description}...")
    result = subprocess.run(cmd, text=True, capture_output=True)
    if result.returncode != 0:
        print(f"Error running {description}:")
        print(result.stderr)
        return False
    
    print(result.stdout)
    return True

def prepare_sonar():
    """Prepare all files for SonarQube analysis"""
    # 1. Generate coverage XML
    if not run_command(["python", "scripts/sonar_coverage.py"], "coverage generation"):
        return 1
    
    # 2. Generate test results XML
    if not run_command(["python", "scripts/sonar_test_results.py"], "test results generation"):
        return 1
    
    print("\nSuccessfully prepared all files for SonarQube analysis.")
    print("You can now run SonarQube analysis.")
    return 0

if __name__ == "__main__":
    sys.exit(prepare_sonar())
