#!/usr/bin/env python3
"""
Script to generate coverage reports specifically formatted for SonarQube.
"""
import os
import sys
import subprocess
import xml.etree.ElementTree as ET

def run_coverage():
    """Run pytest with coverage and generate XML report"""
    # Ensure coverage-reports directory exists
    os.makedirs("coverage-reports", exist_ok=True)
    
    # Run coverage with relative paths
    cmd = [
        "python", "-m", "pytest",
        "--cov=readability", "--cov=cli",
        "--cov-report=xml:coverage-reports/coverage.xml"
    ]
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print("Coverage test run failed")
        return result.returncode
    
    # Post-process the XML to fix paths for SonarQube
    fix_coverage_xml("coverage-reports/coverage.xml")
    return 0

def fix_coverage_xml(xml_path):
    """Fix the coverage XML file to use relative paths and correct filenames"""
    print(f"Fixing coverage XML file: {xml_path}")
    try:
        # Parse the XML file
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        # Fix the source paths - replace absolute paths with relative ones
        sources_elem = root.find("sources")
        if sources_elem is not None:
            # Remove existing source elements
            for source in list(sources_elem):
                sources_elem.remove(source)
            
            # Add a single source element pointing to project root
            source = ET.SubElement(sources_elem, "source")
            source.text = "."
        
        # Fix class paths - ensure they include the module prefix
        packages = root.findall(".//package")
        for package in packages:
            classes = package.findall("./classes/class")
            for cls in classes:
                filename = cls.get("filename")
                if not filename.startswith("cli/") and not filename.startswith("readability/"):
                    # Check if this is a CLI file or readability file based on context
                    # We need to determine which module the file belongs to
                    module = "cli"  # Default assumption for files in the root package
                    
                    # You might need more sophisticated logic here based on your project structure
                    # For now, we'll use a simple approach:
                    # 1. Files like "main.py" are likely CLI files
                    # 2. Files with model-related names are likely readability files
                    readability_patterns = ["model", "parser", "regexps", "utils"]
                    if any(pattern in filename.lower() for pattern in readability_patterns):
                        module = "readability"
                        
                    cls.set("filename", f"{module}/{filename}")
        
        # Save the fixed XML
        tree.write(xml_path)
        print(f"Successfully fixed {xml_path}")
    
    except Exception as e:
        print(f"Error fixing coverage XML: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(run_coverage())
