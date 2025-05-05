#!/usr/bin/env python3
"""
Script to fix coverage XML file for SonarQube.
"""
import os
import sys
import re

def fix_coverage_xml(xml_path):
    """Fix the coverage XML file to use relative paths and correct filenames"""
    print(f"Fixing coverage XML file: {xml_path}")
    try:
        # Read the XML file as text
        with open(xml_path, 'r') as f:
            content = f.read()
        
        # Replace absolute paths in sources with relative path
        content = re.sub(
            r'<sources>.*?</sources>',
            '<sources>\n\t\t<source>.</source>\n\t</sources>',
            content,
            flags=re.DOTALL
        )
        
        # Add module prefix to filenames
        content = re.sub(
            r'<class name="(errors|main)\.py" filename="(errors|main)\.py"',
            r'<class name="\1.py" filename="cli/\2.py"',
            content
        )
        
        content = re.sub(
            r'<class name="(models|parser|regexps|utils)\.py" filename="(models|parser|regexps|utils)\.py"',
            r'<class name="\1.py" filename="readability/\2.py"',
            content
        )
        
        # Write the modified content back to the file
        with open(xml_path, 'w') as f:
            f.write(content)
        
        print(f"Successfully fixed {xml_path}")
    
    except Exception as e:
        print(f"Error fixing coverage XML: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    if len(sys.argv) > 1:
        xml_path = sys.argv[1]
    else:
        xml_path = "coverage-reports/coverage.xml"
    
    sys.exit(fix_coverage_xml(xml_path))
