"""Tests for Content Cleaning functionality in Python Readability."""

import pytest
from pathlib import Path

from .test_categories import FunctionalArea, get_test_cases_by_functional_area
from .helpers import test_individual_case


# Get all test cases for Content Cleaning
CONTENT_CLEANING_TESTS = get_test_cases_by_functional_area(FunctionalArea.CONTENT_CLEANING)

# Create parameterized test cases with marks
test_cases_with_marks = [
    pytest.param(case_name, id=case_name)
    for case_name in CONTENT_CLEANING_TESTS
]


@pytest.mark.area_content_cleaning
@pytest.mark.parametrize("case_name", test_cases_with_marks)
def test_content_cleaning(case_name):
    """Run tests for content cleaning.
    
    Args:
        case_name: Name of the test case
    """
    case_dir = Path(__file__).parent / "test-pages" / case_name
    test_individual_case(case_dir)
