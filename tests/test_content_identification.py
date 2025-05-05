"""Tests for Content Identification functionality in Python Readability."""

import pytest
from pathlib import Path

from .test_categories import FunctionalArea, get_test_cases_by_functional_area
from .helpers import test_individual_case


# Get all test cases for Content Identification
CONTENT_IDENTIFICATION_TESTS = get_test_cases_by_functional_area(FunctionalArea.CONTENT_IDENTIFICATION)

# Create parameterized test cases with marks
test_cases_with_marks = [
    pytest.param(case_name, id=case_name)
    for case_name in CONTENT_IDENTIFICATION_TESTS
]


@pytest.mark.area_content_identification
@pytest.mark.parametrize("case_name", test_cases_with_marks)
def test_content_identification(case_name):
    """Run tests for content identification.
    
    Args:
        case_name: Name of the test case
    """
    case_dir = Path(__file__).parent / "test-pages" / case_name
    test_individual_case(case_dir)
