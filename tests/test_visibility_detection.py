"""Tests for Visibility Detection functionality in Python Readability."""

import pytest
from pathlib import Path

from .test_categories import FunctionalArea, get_test_cases_by_functional_area
from .helpers import test_individual_case


# Get all test cases for Visibility Detection
VISIBILITY_DETECTION_TESTS = get_test_cases_by_functional_area(FunctionalArea.VISIBILITY_DETECTION)

# Create parameterized test cases with marks
test_cases_with_marks = [
    pytest.param(case_name, id=case_name)
    for case_name in VISIBILITY_DETECTION_TESTS
]


@pytest.mark.area_visibility_detection
@pytest.mark.parametrize("case_name", test_cases_with_marks)
def test_visibility_detection(case_name):
    """Run tests for visibility detection.
    
    Args:
        case_name: Name of the test case
    """
    case_dir = Path(__file__).parent / "test-pages" / case_name
    test_individual_case(case_dir)
