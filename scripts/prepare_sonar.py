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
    try:
        # Run the command and capture output in real-time
        process = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        # Print output in real-time
        for line in process.stdout:
            print(line, end='')
        
        # Wait for the process to complete
        process.wait()
        
        # Check if there was an error
        if process.returncode != 0:
            print(f"Error running {description} (exit code {process.returncode}):")
            for line in process.stderr:
                print(line, end='')
            return False
        
        return True
    except Exception as e:
        print(f"Error running {description}: {e}")
        return False

def prepare_sonar():
    """Prepare all files for SonarQube analysis"""
    # Since we already have the coverage XML file, just fix it
    if not run_command(["python", "scripts/fix_coverage.py"], "coverage XML fix"):
        return 1
    
    # Generate test results XML
    if not run_command(["python", "scripts/sonar_test_results.py"], "test results generation"):
        return 1
    
    print("\nSuccessfully prepared all files for SonarQube analysis.")
    print("You can now run SonarQube analysis.")
    return 0

if __name__ == "__main__":
    sys.exit(prepare_sonar())
