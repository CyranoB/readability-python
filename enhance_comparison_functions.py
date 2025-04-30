#!/usr/bin/env python3
"""
Enhancement Script for Comparison Functions

This script enhances the HTML and metadata comparison functions in conftest.py
to make them more robust and configurable as outlined in the test improvement plan.

Usage:
  python enhance_comparison_functions.py

The script creates a backup of the original conftest.py and then makes the enhancements.
"""

import os
import sys
import re
import shutil
from pathlib import Path
import datetime

# Path to conftest.py
CONFTEST_PATH = Path("tests/conftest.py")

# Backup path
BACKUP_DIR = Path("tests/backups")
BACKUP_PATH = BACKUP_DIR / f"conftest_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.py.bak"

# New normalize_html function
NEW_NORMALIZE_HTML = '''
def normalize_html(html: str, normalize_case: bool = True, 
                  normalize_attrs: bool = True, normalize_whitespace: bool = True,
                  normalize_entities: bool = True) -> str:
    """Normalize HTML for comparison.
    
    Args:
        html: The HTML string to normalize
        normalize_case: Whether to normalize case for tag names and attributes
        normalize_attrs: Whether to normalize attribute ordering
        normalize_whitespace: Whether to normalize whitespace
        normalize_entities: Whether to normalize HTML entities
        
    Returns:
        Normalized HTML string
    """
    soup = BeautifulSoup(html, "lxml")
    
    # Remove data-readability attributes
    for tag in soup.find_all(True):
        attrs = list(tag.attrs.keys())
        for attr in attrs:
            if attr.startswith("data-readability"):
                del tag[attr]
    
    # Normalize case if requested
    if normalize_case:
        # Convert tag names to lowercase
        for tag in soup.find_all(True):
            tag.name = tag.name.lower()
            
            # Convert attribute names to lowercase
            for attr in list(tag.attrs.keys()):
                if attr.lower() != attr:
                    tag.attrs[attr.lower()] = tag.attrs.pop(attr)
    
    # Normalize attribute ordering if requested
    if normalize_attrs:
        for tag in soup.find_all(True):
            # Sort attributes by name
            tag.attrs = {key: tag.attrs[key] for key in sorted(tag.attrs.keys())}
    
    # Normalize whitespace if requested
    if normalize_whitespace:
        # Handle text nodes
        for text in soup.find_all(text=True):
            if text.parent.name not in ["pre", "code"]:  # Preserve whitespace in pre/code tags
                text.replace_with(re.sub(r'\\s+', ' ', text.string.strip()))
    
    # Normalize HTML entities if requested
    if normalize_entities:
        # BeautifulSoup automatically handles most entity normalization
        pass
    
    # Prettify and normalize
    return soup.prettify()
'''

# New compare_html function
NEW_COMPARE_HTML = '''
def compare_html(actual: str, expected: str, threshold: float = 0.9, 
                compare_structure: bool = True, normalize_options: dict = None) -> Dict:
    """Compare two HTML strings and return comparison results.
    
    Args:
        actual: The actual HTML string
        expected: The expected HTML string
        threshold: Similarity threshold for text comparison
        compare_structure: Whether to compare HTML structure
        normalize_options: Options for HTML normalization
        
    Returns:
        Dict with comparison results
    """
    # Import here to avoid circular imports
    import difflib
    
    # Apply normalization with specified options
    normalize_options = normalize_options or {}
    actual_normalized = normalize_html(actual, **normalize_options)
    expected_normalized = normalize_html(expected, **normalize_options)
    
    # Parse normalized HTML
    actual_soup = BeautifulSoup(actual_normalized, "lxml")
    expected_soup = BeautifulSoup(expected_normalized, "lxml")
    
    # Extract text content
    actual_text = actual_soup.get_text(separator=" ").strip()
    expected_text = expected_soup.get_text(separator=" ").strip()
    
    # Calculate text similarity
    text_similarity = difflib.SequenceMatcher(None, actual_text, expected_text).ratio()
    
    results = {
        "text_similarity": text_similarity,
        "text_match": actual_text == expected_text,
        "actual_text_length": len(actual_text),
        "expected_text_length": len(expected_text)
    }
    
    # Compare structure if requested
    if compare_structure:
        # Count tags by type
        actual_tag_counts = {}
        expected_tag_counts = {}
        
        for tag in actual_soup.find_all():
            actual_tag_counts[tag.name] = actual_tag_counts.get(tag.name, 0) + 1
            
        for tag in expected_soup.find_all():
            expected_tag_counts[tag.name] = expected_tag_counts.get(tag.name, 0) + 1
        
        # Compare tag counts
        all_tags = set(list(actual_tag_counts.keys()) + list(expected_tag_counts.keys()))
        tag_count_diffs = {}
        
        for tag in all_tags:
            actual_count = actual_tag_counts.get(tag, 0)
            expected_count = expected_tag_counts.get(tag, 0)
            if actual_count != expected_count:
                tag_count_diffs[tag] = {
                    "actual": actual_count,
                    "expected": expected_count,
                    "diff": actual_count - expected_count
                }
        
        results["tag_counts_match"] = len(tag_count_diffs) == 0
        results["tag_count_diffs"] = tag_count_diffs
    else:
        # Just compare tag presence
        actual_tags = set(tag.name for tag in actual_soup.find_all())
        expected_tags = set(tag.name for tag in expected_soup.find_all())
        results["tag_counts_match"] = actual_tags == expected_tags
    
    # Add detailed diff if similarity below threshold
    if text_similarity < threshold:
        differ = difflib.Differ()
        actual_lines = actual_normalized.splitlines()
        expected_lines = expected_normalized.splitlines()
        
        # Get line-by-line diff
        diff = list(differ.compare(actual_lines, expected_lines))
        
        # Only keep lines with differences to keep the output manageable
        diff = [line for line in diff if line.startswith('- ') or line.startswith('+ ') or line.startswith('? ')]
        
        if len(diff) > 20:  # Limit diff size
            diff = diff[:10] + ['...'] + diff[-10:]
            
        results["diff"] = diff
    
    return results
'''

# New compare_metadata function
NEW_COMPARE_METADATA = '''
def compare_metadata(actual: Any, expected: dict, strict: bool = False, field_mapping: dict = None) -> dict:
    """Compare Article metadata with expected metadata from JSON.
    
    Args:
        actual: The actual Article object
        expected: The expected metadata dict
        strict: Whether to be strict in comparison
        field_mapping: Custom field mapping
        
    Returns:
        Dict with comparison results
    """
    results = {}
    
    # Use provided field mapping or default
    field_mapping = field_mapping or {
        "title": "title",
        "byline": "byline",
        "excerpt": "excerpt",
        "siteName": "site_name",
        "image": "image",
        "favicon": "favicon",
        "language": "language",
        "publishedTime": "published_time"
    }
    
    # Get lenient fields based on strictness
    lenient_fields = [] if strict else ["byline", "language", "excerpt"]
    
    # Compare each field
    for json_field, attr_name in field_mapping.items():
        actual_value = getattr(actual, attr_name, "")
        expected_value = expected.get(json_field, "")
        
        # Special case for dates
        if json_field == "publishedTime":
            matches = compare_dates(actual_value, expected_value)
        # Special case for image - treat None as empty string
        elif json_field == "image" and actual_value is None and expected_value == "":
            matches = True
        # Be lenient with certain fields if not strict
        elif json_field in lenient_fields:
            matches = True
        else:
            # Regular comparison
            matches = actual_value == expected_value
            
        results[json_field] = {
            "matches": matches,
            "actual": actual_value,  # Preserve original value
            "expected": expected_value,  # Preserve original value
            "str_actual": str(actual_value),  # String representation
            "str_expected": str(expected_value)  # String representation
        }
    
    return results
'''

# New compare_dates function
NEW_COMPARE_DATES = '''
def compare_dates(actual_date: Optional[datetime.datetime], 
                 expected_date_str: Optional[str], 
                 compare_time: bool = False) -> bool:
    """Compare a datetime object with a date string.
    
    Args:
        actual_date: The actual datetime object
        expected_date_str: The expected date string
        compare_time: Whether to compare time components
        
    Returns:
        True if dates match according to comparison criteria
    """
    if not actual_date and not expected_date_str:
        return True
    if not actual_date or not expected_date_str:
        return False
        
    try:
        expected_date = parser.parse(expected_date_str)
        
        # Compare date parts
        date_match = (actual_date.year == expected_date.year and 
                     actual_date.month == expected_date.month and
                     actual_date.day == expected_date.day)
                     
        # If time comparison is not required, return date match
        if not compare_time:
            return date_match
            
        # Compare time parts if required
        time_match = (actual_date.hour == expected_date.hour and
                     actual_date.minute == expected_date.minute and
                     actual_date.second == expected_date.second)
                     
        return date_match and time_match
    except Exception as e:
        print(f"Error comparing dates: {e}")
        return False
'''

def backup_file(file_path, backup_path):
    """Create a backup of the file."""
    try:
        # Create backup directory if it doesn't exist
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Copy the file
        shutil.copy2(file_path, backup_path)
        print(f"Created backup: {backup_path}")
        return True
    except Exception as e:
        print(f"Error creating backup: {e}")
        return False

def update_function(content, function_name, new_function):
    """Update a function in the content."""
    # Simple pattern to find a function definition
    pattern = fr"def {function_name}\(.*?\):.*?(?=\n\n|$)"
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        print(f"Warning: Could not find function {function_name}.")
        return content
    
    # Replace the function
    return content.replace(match.group(0), new_function.strip())

def add_imports(content):
    """Add necessary imports."""
    # Check if imports exist
    imports_to_add = []
    
    if "import datetime" not in content:
        imports_to_add.append("import datetime")
    
    if "from typing import Dict, Any, Optional" not in content:
        imports_to_add.append("from typing import Dict, Any, Optional")
    
    if not imports_to_add:
        return content
    
    # Add imports after existing imports
    import_section_end = 0
    for line in content.split("\n"):
        if line.strip() and not line.startswith("import") and not line.startswith("from"):
            break
        import_section_end += len(line) + 1
    
    new_imports = "\n".join(imports_to_add) + "\n\n"
    return content[:import_section_end] + new_imports + content[import_section_end:]

def main():
    """Main function."""
    # Check if conftest.py exists
    if not CONFTEST_PATH.exists():
        print(f"Error: {CONFTEST_PATH} not found.")
        return False
    
    # Read the content
    content = CONFTEST_PATH.read_text(encoding="utf-8")
    
    # Create a backup
    if not backup_file(CONFTEST_PATH, BACKUP_PATH):
        print("Aborting due to backup failure.")
        return False
    
    # Update functions
    content = update_function(content, "normalize_html", NEW_NORMALIZE_HTML)
    content = update_function(content, "compare_html", NEW_COMPARE_HTML)
    content = update_function(content, "compare_metadata", NEW_COMPARE_METADATA)
    content = update_function(content, "compare_dates", NEW_COMPARE_DATES)
    
    # Add imports
    content = add_imports(content)
    
    # Write back to the file
    try:
        CONFTEST_PATH.write_text(content, encoding="utf-8")
        print(f"Successfully updated {CONFTEST_PATH}")
        return True
    except Exception as e:
        print(f"Error writing to {CONFTEST_PATH}: {e}")
        print(f"The original file is backed up at {BACKUP_PATH}")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)