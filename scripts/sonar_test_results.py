#!/usr/bin/env python3
"""
Script to generate JUnit XML test results for SonarQube.
"""
import os
import sys
import subprocess

def generate_test_results():
    """Run pytest with JUnit XML output"""
    # Ensure directory exists
    os.makedirs("test-reports", exist_ok=True)
    
    cmd = [
        "python", "-m", "pytest",
        "--junitxml=test-reports/test-results.xml"
    ]
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    return result.returncode

if __name__ == "__main__":
    sys.exit(generate_test_results())
