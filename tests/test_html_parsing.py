"""Tests for HTML Parsing functionality in Python Readability."""

import pytest
from pathlib import Path

from .test_categories import FunctionalArea, get_test_cases_by_functional_area
from .helpers import test_individual_case


# Get all test cases for HTML Parsing
HTML_PARSING_TESTS = get_test_cases_by_functional_area(FunctionalArea.HTML_PARSING)

# Create parameterized test cases with marks
test_cases_with_marks = [
    pytest.param(case_name, id=case_name)
    for case_name in HTML_PARSING_TESTS
]


@pytest.mark.area_html_parsing
@pytest.mark.parametrize("case_name", test_cases_with_marks)
def test_html_parsing(case_name):
    """Run tests for HTML parsing.
    
    Args:
        case_name: Name of the test case
    """
    case_dir = Path(__file__).parent / "test-pages" / case_name
    test_individual_case(case_dir)
