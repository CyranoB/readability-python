"""Test categories for Python Readability."""

from enum import Enum
from typing import Dict, List, Set, Tuple

# Category enumerations
class FunctionalArea(Enum):
    """Functional areas for test categorization."""
    HTML_PARSING = "HTML Parsing"
    METADATA_EXTRACTION = "Metadata Extraction"
    CONTENT_IDENTIFICATION = "Content Identification"
    CONTENT_CLEANING = "Content Cleaning"
    URL_HANDLING = "URL Handling"
    VISIBILITY_DETECTION = "Visibility Detection"
    TEXT_NORMALIZATION = "Text Normalization"
    REAL_WORLD = "Real-world Websites"

class Criticality(Enum):
    """Criticality levels for test categorization."""
    P0 = "P0 (Critical)"
    P1 = "P1 (High)"
    P2 = "P2 (Medium)"
    P3 = "P3 (Low)"

class TestType(Enum):
    """Test types for test categorization."""
    BASIC = "Basic"
    FEATURE = "Feature"
    EDGE_CASE = "Edge Case"
    REAL_WORLD = "Real-world"

# Test case categorization
TEST_CASE_CATEGORIES: Dict[str, Tuple[FunctionalArea, Criticality, TestType, str]] = {
    # Format: "test_case_name": (FunctionalArea, Criticality, TestType, "Description")
    
    # Basic test cases
    "001": (FunctionalArea.CONTENT_IDENTIFICATION, Criticality.P0, TestType.BASIC, 
            "Basic article extraction with code blocks and formatting"),
    "002": (FunctionalArea.CONTENT_IDENTIFICATION, Criticality.P0, TestType.BASIC, 
            "Basic article extraction with simple content"),
    
    # Metadata extraction test cases
    "003-metadata-preferred": (FunctionalArea.METADATA_EXTRACTION, Criticality.P1, TestType.FEATURE, 
                              "Tests preference for metadata in meta tags"),
    "004-metadata-space-separated-properties": (FunctionalArea.METADATA_EXTRACTION, Criticality.P1, TestType.FEATURE, 
                                              "Tests handling of space-separated properties in metadata"),
    "metadata-content-missing": (FunctionalArea.METADATA_EXTRACTION, Criticality.P1, TestType.EDGE_CASE, 
                                "Tests handling of missing metadata"),
    
    # URL handling test cases
    "base-url": (FunctionalArea.URL_HANDLING, Criticality.P1, TestType.FEATURE, 
                "Tests conversion of relative URLs to absolute URLs"),
    "base-url-base-element": (FunctionalArea.URL_HANDLING, Criticality.P1, TestType.FEATURE, 
                             "Tests handling of base element for URL resolution"),
    "base-url-base-element-relative": (FunctionalArea.URL_HANDLING, Criticality.P1, TestType.FEATURE, 
                                      "Tests handling of relative URLs in base element"),
    
    # Content cleaning test cases
    "basic-tags-cleaning": (FunctionalArea.CONTENT_CLEANING, Criticality.P1, TestType.FEATURE, 
                           "Tests cleaning of basic HTML tags"),
    "js-link-replacement": (FunctionalArea.CONTENT_CLEANING, Criticality.P2, TestType.FEATURE, 
                           "Tests handling of JavaScript links"),
    "keep-images": (FunctionalArea.CONTENT_CLEANING, Criticality.P1, TestType.FEATURE, 
                   "Tests preservation of image elements in content"),
    "missing-paragraphs": (FunctionalArea.CONTENT_CLEANING, Criticality.P1, TestType.EDGE_CASE, 
                          "Tests handling of content without proper paragraph tags"),
    "remove-script-tags": (FunctionalArea.CONTENT_CLEANING, Criticality.P0, TestType.FEATURE, 
                          "Tests removal of script tags from content"),
    "replace-brs": (FunctionalArea.CONTENT_CLEANING, Criticality.P1, TestType.FEATURE, 
                   "Tests replacement of BR tags with paragraph breaks"),
    "replace-font-tags": (FunctionalArea.CONTENT_CLEANING, Criticality.P1, TestType.FEATURE, 
                         "Tests replacement of font tags with span tags"),
    
    # HTML parsing test cases
    "comment-inside-script-parsing": (FunctionalArea.HTML_PARSING, Criticality.P2, TestType.EDGE_CASE, 
                                     "Tests handling of comments inside script tags"),
    "svg-parsing": (FunctionalArea.HTML_PARSING, Criticality.P2, TestType.EDGE_CASE, 
                   "Tests handling of SVG elements in content"),
    
    # Visibility detection test cases
    "hidden-nodes": (FunctionalArea.VISIBILITY_DETECTION, Criticality.P0, TestType.FEATURE, 
                    "Tests exclusion of hidden elements"),
    "remove-aria-hidden": (FunctionalArea.VISIBILITY_DETECTION, Criticality.P1, TestType.FEATURE, 
                          "Tests handling of aria-hidden attribute"),
    
    # Text normalization test cases
    "normalize-spaces": (FunctionalArea.TEXT_NORMALIZATION, Criticality.P1, TestType.FEATURE, 
                        "Tests normalization of whitespace in content"),
    "rtl-3": (FunctionalArea.TEXT_NORMALIZATION, Criticality.P2, TestType.EDGE_CASE, 
             "Tests handling of right-to-left text"),
    "rtl-4": (FunctionalArea.TEXT_NORMALIZATION, Criticality.P2, TestType.EDGE_CASE, 
             "Tests handling of right-to-left text"),
    "qq": (FunctionalArea.TEXT_NORMALIZATION, Criticality.P2, TestType.EDGE_CASE, 
          "Tests handling of non-Latin character sets"),
    
    # Real-world website test cases
    "aclu": (FunctionalArea.REAL_WORLD, Criticality.P3, TestType.REAL_WORLD, 
            "Tests extraction from ACLU article"),
    "aktualne": (FunctionalArea.REAL_WORLD, Criticality.P3, TestType.REAL_WORLD, 
                "Tests extraction from Aktualne news article"),
    "archive-of-our-own": (FunctionalArea.REAL_WORLD, Criticality.P3, TestType.REAL_WORLD, 
                          "Tests extraction from Archive of Our Own content"),
    "ars-1": (FunctionalArea.REAL_WORLD, Criticality.P3, TestType.REAL_WORLD, 
             "Tests extraction from Ars Technica article"),
    "bbc-1": (FunctionalArea.REAL_WORLD, Criticality.P3, TestType.REAL_WORLD, 
             "Tests extraction from BBC article"),
    "blogger": (FunctionalArea.REAL_WORLD, Criticality.P3, TestType.REAL_WORLD, 
               "Tests extraction from Blogger post"),
    "breitbart": (FunctionalArea.REAL_WORLD, Criticality.P3, TestType.REAL_WORLD, 
                 "Tests extraction from Breitbart article"),
    "ehow-2": (FunctionalArea.REAL_WORLD, Criticality.P2, TestType.REAL_WORLD, 
              "Tests extraction from eHow article"),
    "herald-sun-1": (FunctionalArea.REAL_WORLD, Criticality.P2, TestType.REAL_WORLD, 
                    "Tests extraction from Herald Sun article"),
    "medium-1": (FunctionalArea.REAL_WORLD, Criticality.P0, TestType.REAL_WORLD, 
                "Tests extraction from Medium article"),
    "medium-2": (FunctionalArea.REAL_WORLD, Criticality.P1, TestType.REAL_WORLD, 
                "Tests extraction from another Medium article"),
    "mozilla-1": (FunctionalArea.REAL_WORLD, Criticality.P0, TestType.REAL_WORLD, 
                 "Tests extraction from Mozilla documentation"),
    "nytimes-1": (FunctionalArea.REAL_WORLD, Criticality.P0, TestType.REAL_WORLD, 
                 "Tests extraction from New York Times article"),
    "wikipedia": (FunctionalArea.REAL_WORLD, Criticality.P0, TestType.REAL_WORLD, 
                 "Tests extraction from Wikipedia article"),
}

# Helper functions to get test cases by category
def get_test_cases_by_functional_area(area: FunctionalArea) -> List[str]:
    """Get all test cases for a specific functional area.
    
    Args:
        area: The functional area to filter by
        
    Returns:
        A list of test case names
    """
    return [name for name, (func_area, _, _, _) in TEST_CASE_CATEGORIES.items() 
            if func_area == area]

def get_test_cases_by_criticality(criticality: Criticality) -> List[str]:
    """Get all test cases for a specific criticality level.
    
    Args:
        criticality: The criticality level to filter by
        
    Returns:
        A list of test case names
    """
    return [name for name, (_, crit, _, _) in TEST_CASE_CATEGORIES.items() 
            if crit == criticality]

def get_test_cases_by_test_type(test_type: TestType) -> List[str]:
    """Get all test cases for a specific test type.
    
    Args:
        test_type: The test type to filter by
        
    Returns:
        A list of test case names
    """
    return [name for name, (_, _, typ, _) in TEST_CASE_CATEGORIES.items() 
            if typ == test_type]

# Coverage analysis functions
def get_coverage_by_functional_area() -> Dict[FunctionalArea, Dict[Criticality, int]]:
    """Get test coverage by functional area and criticality.
    
    Returns:
        A dictionary mapping functional areas to criticality counts
    """
    coverage = {area: {crit: 0 for crit in Criticality} for area in FunctionalArea}
    
    for _, (area, crit, _, _) in TEST_CASE_CATEGORIES.items():
        coverage[area][crit] += 1
        
    return coverage

def get_coverage_by_test_type() -> Dict[TestType, int]:
    """Get test coverage by test type.
    
    Returns:
        A dictionary mapping test types to counts
    """
    coverage = {typ: 0 for typ in TestType}
    
    for _, (_, _, typ, _) in TEST_CASE_CATEGORIES.items():
        coverage[typ] += 1
        
    return coverage

def print_coverage_summary():
    """Print a summary of test coverage."""
    # Functional area coverage
    area_coverage = get_coverage_by_functional_area()
    print("Coverage by Functional Area:")
    print(f"{'Functional Area':<25} {'P0':<5} {'P1':<5} {'P2':<5} {'P3':<5} {'Total':<5}")
    print("-" * 50)
    
    for area in FunctionalArea:
        p0 = area_coverage[area][Criticality.P0]
        p1 = area_coverage[area][Criticality.P1]
        p2 = area_coverage[area][Criticality.P2]
        p3 = area_coverage[area][Criticality.P3]
        total = p0 + p1 + p2 + p3
        print(f"{area.value:<25} {p0:<5} {p1:<5} {p2:<5} {p3:<5} {total:<5}")
        
    # Test type coverage
    type_coverage = get_coverage_by_test_type()
    print("\nCoverage by Test Type:")
    total = sum(type_coverage.values())
    for typ, count in type_coverage.items():
        percentage = count / total * 100 if total > 0 else 0
        print(f"{typ.value:<15}: {count:<5} ({percentage:.1f}%)")

# Verification functions
def verify_test_case_existence():
    """Verify that all categorized test cases exist in the test directory."""
    from pathlib import Path
    
    test_dir = Path(__file__).parent / "test-pages"
    missing_cases = []
    
    for case_name in TEST_CASE_CATEGORIES:
        case_dir = test_dir / case_name
        if not case_dir.exists():
            missing_cases.append(case_name)
            
    if missing_cases:
        print(f"Warning: The following categorized test cases do not exist: {missing_cases}")
    else:
        print("All categorized test cases exist in the test directory.")
        
    # Check for uncategorized test cases
    all_test_cases = [d.name for d in test_dir.iterdir() if d.is_dir()]
    uncategorized_cases = [name for name in all_test_cases if name not in TEST_CASE_CATEGORIES]
    
    if uncategorized_cases:
        print(f"Warning: The following test cases are not categorized: {uncategorized_cases}")
    else:
        print("All test cases in the test directory are categorized.")

# Test case migration recommendations
def get_migration_recommendations() -> Dict[str, List[str]]:
    """Get recommendations for test case migration from Go implementation.
    
    Returns:
        A dictionary mapping priority levels to lists of test cases
    """
    return {
        "high_priority": [
            # Already migrated
            # "base-url-base-element",
            # "base-url-base-element-relative",
            # "remove-aria-hidden",
            # "replace-font-tags",
            # "medium-2"
        ],
        "medium_priority": [
            # Already migrated
            # "rtl-3",
            # "rtl-4",
            # "qq",
            # "js-link-replacement",
            # "ehow-2",
            # "herald-sun-1"
        ],
        "low_priority": [
            # Already migrated
            # "aclu",
            # "aktualne",
            # "archive-of-our-own",
            # "ars-1",
            # "bbc-1",
            # "blogger",
            # "breitbart"
        ]
    }

if __name__ == "__main__":
    # Print coverage summary when run as a script
    print_coverage_summary()
    verify_test_case_existence()
