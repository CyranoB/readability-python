# Test Case Comparison: Go vs Python Implementation

This document compares the test cases between the original Go implementation and the Python port to identify any gaps in test coverage.

## Methodology

1. List all test case directories in `go-readability/test-pages/`
2. List all test case directories in `tests/test-pages/`
3. Compare the two sets to identify:
   - Test cases present in both implementations
   - Test cases missing from the Python implementation
   - Test cases unique to the Python implementation (if any)
4. For each test case, verify the presence of required files:
   - `source.html`: Input HTML
   - `expected.html`: Expected output HTML
   - `expected-metadata.json`: Expected metadata (if applicable)

## Test Case Inventory

### Go Implementation Test Cases

Based on the file structure, the following test cases are present in the Go implementation:

1. base-url-base-element
2. base-url-base-element-relative
3. ehow-2
4. herald-sun-1
5. js-link-replacement
6. keep-images
7. medium-2
8. metadata-content-missing
9. mozilla-1
10. qq
11. remove-aria-hidden
12. replace-font-tags
13. rtl-3
14. rtl-4

### Python Implementation Test Cases

Based on the file structure, the following test cases are present in the Python implementation:

1. 001
2. 002
3. 003-metadata-preferred
4. 004-metadata-space-separated-properties
5. base-url
6. basic-tags-cleaning
7. comment-inside-script-parsing
8. hidden-nodes
9. keep-images
10. medium-1
11. metadata-content-missing
12. missing-paragraphs
13. mozilla-1
14. normalize-spaces
15. nytimes-1
16. remove-script-tags
17. replace-brs
18. svg-parsing

## Comparison Results

### Test Cases Present in Both Implementations

1. keep-images
2. metadata-content-missing
3. mozilla-1

### Test Cases Missing from Python Implementation

1. base-url-base-element
2. base-url-base-element-relative
3. ehow-2
4. herald-sun-1
5. js-link-replacement
6. medium-2
7. qq
8. remove-aria-hidden
9. replace-font-tags
10. rtl-3
11. rtl-4

### Test Cases Unique to Python Implementation

1. 001
2. 002
3. 003-metadata-preferred
4. 004-metadata-space-separated-properties
5. base-url
6. basic-tags-cleaning
7. comment-inside-script-parsing
8. hidden-nodes
9. medium-1
10. missing-paragraphs
11. normalize-spaces
12. nytimes-1
13. remove-script-tags
14. replace-brs
15. svg-parsing

## Analysis

The comparison reveals significant differences between the test suites:

1. **Limited Overlap**: Only 3 test cases are common between both implementations.
2. **Missing Go Test Cases**: 11 test cases from the Go implementation are not present in the Python implementation.
3. **Python-Specific Test Cases**: The Python implementation has 15 test cases not present in the Go implementation.

This suggests that:

1. The Python implementation has developed its own test suite rather than directly porting all test cases from Go.
2. There may be important test scenarios in the Go implementation that should be migrated to ensure compatibility.
3. The Python implementation may be testing additional scenarios not covered in the Go implementation.

## Recommendations

1. **Migrate Missing Go Test Cases**: Copy the 11 missing test cases from the Go implementation to ensure compatibility testing.
2. **Review Test Case Purpose**: For each test case, document what specific feature or edge case it's testing to ensure comprehensive coverage.
3. **Consolidate Similar Test Cases**: Identify if any of the unique test cases in each implementation are testing similar functionality and could be consolidated.
4. **Update Parameterized Tests**: After migration, update the parameterized test list in `test_readability.py` to include all test cases.

## Migration Plan

For each missing test case, perform the following steps:

1. Create a directory in `tests/test-pages/` with the same name as the Go test case
2. Copy `source.html`, `expected.html`, and `expected-metadata.json` (if present) from the Go test case directory
3. Add the test case name to the parameterized test list in `test_readability.py`
4. Run the test to verify it works or identify any issues

### Priority Order for Migration

Based on the importance of features being tested:

1. base-url-base-element and base-url-base-element-relative (URL handling)
2. replace-font-tags (HTML cleaning)
3. js-link-replacement (JavaScript handling)
4. medium-2 (Real-world site testing)
5. qq (Non-Latin character handling)
6. rtl-3 and rtl-4 (Right-to-left text handling)
7. remove-aria-hidden (Accessibility attribute handling)
8. ehow-2 and herald-sun-1 (Additional real-world site testing)