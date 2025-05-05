"""Tests for Metadata Extraction functionality in Python Readability."""

import pytest
from pathlib import Path

from .test_categories import FunctionalArea, get_test_cases_by_functional_area
from .helpers import test_individual_case


# Get all test cases for Metadata Extraction
METADATA_EXTRACTION_TESTS = get_test_cases_by_functional_area(FunctionalArea.METADATA_EXTRACTION)

# Create parameterized test cases with marks
test_cases_with_marks = [
    pytest.param(case_name, id=case_name)
    for case_name in METADATA_EXTRACTION_TESTS
]


@pytest.mark.area_metadata_extraction
@pytest.mark.parametrize("case_name", test_cases_with_marks)
def test_metadata_extraction(case_name):
    """Run tests for metadata extraction.
    
    Args:
        case_name: Name of the test case
    """
    case_dir = Path(__file__).parent / "test-pages" / case_name
    test_individual_case(case_dir)
