"""Debug tools for Python Readability tests."""

import difflib
import json
from pathlib import Path


def generate_html_diff(actual, expected, output_path):
    """Generate an HTML diff for visual comparison.
    
    Args:
        actual: The actual HTML content
        expected: The expected HTML content
        output_path: Path to save the HTML diff
        
    Returns:
        The output path
    """
    diff = difflib.HtmlDiff()
    
    # Split into lines
    actual_lines = actual.splitlines()
    expected_lines = expected.splitlines()
    
    # Generate HTML diff
    diff_html = diff.make_file(
        actual_lines, 
        expected_lines,
        fromdesc="Generated HTML", 
        todesc="Expected HTML"
    )
    
    # Write to file
    output_path.write_text(diff_html, encoding="utf-8")
    
    return output_path


def save_debug_output(test_name, article, expected_html, expected_metadata):
    """Save debug information for a test case.
    
    Args:
        test_name: Name of the test case
        article: The Article object
        expected_html: The expected HTML content
        expected_metadata: The expected metadata
        
    Returns:
        The debug directory path
    """
    debug_dir = Path("tests/debug") / test_name
    debug_dir.mkdir(parents=True, exist_ok=True)
    
    # Save generated HTML
    html_path = debug_dir / "generated.html"
    html_path.write_text(article.content, encoding="utf-8")
    
    # Save expected HTML
    expected_html_path = debug_dir / "expected.html"
    expected_html_path.write_text(expected_html, encoding="utf-8")
    
    # Generate diff
    diff_path = debug_dir / "diff.html"
    generate_html_diff(article.content, expected_html, diff_path)
    
    # Save article metadata
    metadata = {
        "title": article.title,
        "byline": article.byline,
        "excerpt": article.excerpt,
        "site_name": article.site_name,
        "image": article.image,
        "favicon": article.favicon,
        "length": article.length,
        "published_time": str(article.published_time) if article.published_time else None
    }
    
    metadata_path = debug_dir / "metadata.json"
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    
    # Save expected metadata
    expected_metadata_path = debug_dir / "expected-metadata.json"
    expected_metadata_path.write_text(json.dumps(expected_metadata, indent=2), encoding="utf-8")
    
    return debug_dir


def create_debug_directory():
    """Create the debug directory if it doesn't exist."""
    debug_dir = Path("tests/debug")
    debug_dir.mkdir(parents=True, exist_ok=True)
    return debug_dir


def clear_debug_directory():
    """Clear the debug directory."""
    import shutil
    debug_dir = Path("tests/debug")
    if debug_dir.exists():
        shutil.rmtree(debug_dir)
    debug_dir.mkdir(parents=True, exist_ok=True)
    return debug_dir
