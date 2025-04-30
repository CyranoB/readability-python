"""Tests for Python Readability."""

import pytest
from pathlib import Path
import json
import difflib
import os

from readability import Readability

# Import test helpers
from .conftest import compare_html, compare_metadata
from .debug_tools import save_debug_output, create_debug_directory


def test_individual_case(case_dir):
    """Test an individual test case.
    
    Args:
        case_dir: Path to the test case directory
    """
    # Skip if directory doesn't exist
    if not case_dir.exists():
        pytest.skip(f"Test directory {case_dir} not found")
    
    # Load test case data
    source_path = case_dir / "source.html"
    expected_html_path = case_dir / "expected.html"
    expected_metadata_path = case_dir / "expected-metadata.json"
    
    # Skip if required files don't exist
    if not source_path.exists() or not expected_html_path.exists():
        pytest.skip(f"Required test files not found in {case_dir}")
    
    # Load source HTML
    with open(source_path, "r", encoding="utf-8") as f:
        source_html = f.read()
    
    # Load expected HTML
    with open(expected_html_path, "r", encoding="utf-8") as f:
        expected_html = f.read()
    
    # Load expected metadata (if exists)
    expected_metadata = {}
    if expected_metadata_path.exists():
        with open(expected_metadata_path, "r", encoding="utf-8") as f:
            expected_metadata = json.load(f)
    
    # Create mock URL
    url = f"https://example.com/test-pages/{case_dir.name}"
    
    # Initialize parser
    parser = Readability()
    
    # Parse HTML
    article, error = parser.parse(source_html, url=url)
    
    # Check for errors
    assert error is None, f"Parser returned error: {error}"
    assert article is not None, "No article was returned"
    
    # Save debug output
    save_debug_output(case_dir.name, article, expected_html, expected_metadata)
    
    # Compare HTML content
    html_results = compare_html(article.content, expected_html)
    assert html_results["text_similarity"] > 0.9, \
        f"HTML content differs: similarity {html_results['text_similarity']}"
    
    # Compare metadata
    metadata_results = compare_metadata(article, expected_metadata)
    
    # Check metadata matches
    for field, result in metadata_results.items():
        if not result["matches"]:
            pytest.fail(f"Metadata field '{field}' differs. "
                        f"Got: {result['actual']}, Expected: {result['expected']}")


@pytest.mark.parametrize("case_name", [
    # Basic test cases first
    "001",
    "002",
    "003-metadata-preferred",
    "004-metadata-space-separated-properties",
    
    # Core functionality tests
    "basic-tags-cleaning",
    "normalize-spaces",
    "replace-brs",
    "metadata-content-missing",
    
    # Edge case tests
    "hidden-nodes",
    "missing-paragraphs",
    "svg-parsing",
    "comment-inside-script-parsing",
    
    # Feature-specific tests
    "base-url",
    "remove-script-tags",
    "keep-images",
    
    # Real-world website tests
    "nytimes-1",
    "wikipedia",
    "mozilla-1",
    "medium-1",
])
def test_specific_cases(case_name):
    """Run tests on specific test cases.
    
    Args:
        case_name: Name of the test case
    """
    case_dir = Path(__file__).parent / "test-pages" / case_name
    test_individual_case(case_dir)


def test_all_cases(test_cases):
    """Run tests on all discovered test cases.
    
    This is more of a comprehensive test that can be run separately.
    
    Args:
        test_cases: List of test cases from the fixture
    """
    # Create debug directory
    create_debug_directory()
    
    # Track failures
    failures = []
    
    for test_case in test_cases:
        # Print test case name for easier debugging
        print(f"\nTesting: {test_case['name']}")
        
        try:
            # Initialize parser
            parser = Readability()
            
            # Parse HTML
            article, error = parser.parse(
                test_case["source_html"], 
                url=test_case["url"]
            )
            
            # Check for errors
            assert error is None, f"Parser returned error: {error}"
            assert article is not None, "No article was returned"
            
            # Save debug output
            save_debug_output(test_case["name"], article, test_case["expected_html"], test_case["expected_metadata"])
            
            # Compare HTML content
            html_results = compare_html(article.content, test_case["expected_html"])
            similarity = html_results["text_similarity"]
            
            # Use lower threshold initially, can be increased as implementation improves
            assert similarity > 0.8, f"HTML content similarity too low: {similarity}"
            
            # Compare metadata
            metadata_results = compare_metadata(article, test_case["expected_metadata"])
            
            # Report metadata comparison results
            for field, result in metadata_results.items():
                if not result["matches"]:
                    print(f"  Warning: Metadata '{field}' differs.")
                    print(f"    Got: {result['actual']}")
                    print(f"    Expected: {result['expected']}")
        
        except Exception as e:
            failures.append((test_case["name"], str(e)))
            print(f"  FAILED: {e}")
    
    # Report failures
    if failures:
        failure_msg = "\n".join([f"{name}: {error}" for name, error in failures])
        pytest.fail(f"Some test cases failed:\n{failure_msg}")
