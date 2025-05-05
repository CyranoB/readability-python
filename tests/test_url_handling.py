"""Tests for URL Handling functionality in Python Readability."""

import pytest
from pathlib import Path

from .test_categories import FunctionalArea, get_test_cases_by_functional_area
from .helpers import test_individual_case


# Get all test cases for URL Handling
URL_HANDLING_TESTS = get_test_cases_by_functional_area(FunctionalArea.URL_HANDLING)

# Create parameterized test cases with marks
test_cases_with_marks = [
    pytest.param(case_name, id=case_name)
    for case_name in URL_HANDLING_TESTS
]


@pytest.mark.area_url_handling
@pytest.mark.parametrize("case_name", test_cases_with_marks)
def test_url_handling(case_name):
    """Run tests for URL handling.
    
    Args:
        case_name: Name of the test case
    """
    case_dir = Path(__file__).parent / "test-pages" / case_name
    test_individual_case(case_dir)
