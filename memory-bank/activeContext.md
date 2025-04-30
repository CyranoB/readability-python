# Active Context for Python Readability

## Current Work Focus

The current focus of the Python Readability project is on implementing a comprehensive test case categorization and prioritization strategy. This involves:

1. **Test Case Categorization**: Categorizing test cases by functional area, criticality level, and test type to provide a clear understanding of what each test case is testing.
2. **Test Case Migration**: Migrating high-priority test cases from the Go implementation to the Python implementation.
3. **Test Infrastructure Enhancement**: Enhancing the test infrastructure to support categorization and prioritization.
4. **Test Case Verification**: Developing tools to verify that all test cases are properly implemented and categorized.

## Recent Changes

### Test Case Categorization

We've created a comprehensive test case categorization document (`test-case-categorization.md`) that categorizes test cases by:

1. **Functional Area**: HTML Parsing, Metadata Extraction, Content Identification, Content Cleaning, URL Handling, Visibility Detection, Text Normalization, Real-world Websites.
2. **Criticality Level**: P0 (Critical), P1 (High), P2 (Medium), P3 (Low).
3. **Test Type**: Basic, Feature, Edge Case, Real-world.

This categorization provides a clear understanding of what each test case is testing and helps identify gaps in test coverage.

### Test Infrastructure Enhancement

We've enhanced the test infrastructure to support categorization and prioritization:

1. **Test Categories Module**: Created a `tests/test_categories.py` module that defines category enumerations, test case to category mappings, and helper functions to get test cases by category.
2. **Test Runner Enhancement**: Updated `tests/test_readability.py` to use pytest marks for categorization and to support running tests by category.
3. **Test Case Verification Script**: Created a `verify_test_cases.py` script to verify that all test cases are properly implemented and categorized.

### Test Case Migration

We've migrated test cases from the Go implementation to the Python implementation:

1. **High Priority Test Cases**:
   - **base-url-base-element**: Tests handling of base element for URL resolution.
   - **base-url-base-element-relative**: Tests handling of relative URLs in base element.
   - **remove-aria-hidden**: Tests handling of aria-hidden attribute.
   - **replace-font-tags**: Tests replacement of font tags with span tags.
   - **medium-2**: Tests extraction from another Medium article.

2. **Medium Priority Test Cases**:
   - **rtl-3** and **rtl-4**: Tests for right-to-left text handling.
   - **qq**: Test for non-Latin character sets.
   - **js-link-replacement**: Test for JavaScript link handling.
   - **ehow-2** and **herald-sun-1**: Real-world website tests.

3. **Low Priority Test Cases**:
   - **aclu**: Tests extraction from ACLU article.
   - **aktualne**: Tests extraction from Aktualne news article.
   - **archive-of-our-own**: Tests extraction from Archive of Our Own content.
   - **ars-1**: Tests extraction from Ars Technica article.
   - **bbc-1**: Tests extraction from BBC article.
   - **blogger**: Tests extraction from Blogger post.
   - **breitbart**: Tests extraction from Breitbart article.

## Next Steps

### 1. Project Reorganization

We've reorganized the project structure to improve maintainability:

1. **Test Documentation**: Moved all test documentation files to `tests/docs/` directory:
   - test-verification-plan.md
   - test-case-comparison.md
   - test-function-analysis.md
   - comparison-function-analysis.md
   - debug-tools-analysis.md
   - test-improvement-plan.md
   - test-infrastructure-assessment.md
   - test-case-categorization.md
   - testing-README.md

2. **Test Scripts**: Moved all test utility scripts to `tests/scripts/` directory:
   - verify_test_cases.py
   - test-case-migration-script.py
   - enhance_comparison_functions.py

3. **Test Fixtures**: Moved test fixtures to `tests/fixtures/` directory:
   - test.html

4. **Path Updates**: Updated paths in scripts to reflect the new directory structure.

### 2. Create New Test Cases

We've successfully fixed the failing test cases and migrated all the medium and low priority test cases. Now we should focus on creating new test cases to fill the identified gaps:

Based on our gap analysis, we should create new test cases to fill the identified gaps:

1. **HTML Parsing**:
   - malformed-html (P2): Test handling of malformed HTML.
   - html5-elements (P2): Test handling of HTML5 specific elements.

2. **Content Cleaning**:
   - table-handling (P1): Test handling of table elements.
   - form-removal (P1): Test removal of form elements.
   - iframe-handling (P2): Test handling of iframe elements.

3. **Metadata Extraction**:
   - schema-org (P1): Test extraction of schema.org metadata.
   - open-graph (P1): Test extraction of Open Graph protocol metadata.
   - twitter-card (P2): Test extraction of Twitter Card metadata.

4. **Visibility Detection**:
   - css-visibility (P1): Test handling of CSS visibility properties.

### 3. Package for Distribution

Prepare the library for distribution on PyPI by finalizing the packaging configuration in pyproject.toml.

## Recent Updates

### Documentation Updates

We've created comprehensive documentation for the project:

1. **README.md**: Created a detailed README with information about:
   - Project overview and features
   - Installation instructions
   - Usage examples (both library API and CLI)
   - Testing approach with categorization details
   - Test coverage statistics
   - Comparison with the Go implementation
   - Development setup and workflow

2. **CONTRIBUTING.md**: Created guidelines for contributors covering:
   - Code of conduct
   - Getting started with contributions
   - Development environment setup
   - Code style requirements
   - Process for adding new test cases
   - Pull request process
   - Issue reporting guidelines

These documentation updates will make it easier for users to understand and use the library, and for contributors to help improve it.

### Testing Infrastructure Improvements

1. **Fixed Pytest Warnings**: Created a `pytest.ini` file to register all custom marks used in our tests. This eliminates the warnings that were previously shown when running the tests, making the test output cleaner and easier to read.

### CLI Implementation

We've implemented a command-line interface for the library in `cli/main.py` that provides the following features:

1. **Input Options**:
   - URL input: Fetch content from a URL
   - File input: Read content from a local file
   - STDIN input: Read content from standard input (if no URL or file is provided)

2. **Output Options**:
   - Format selection: HTML (default), text (plain text), or JSON (including metadata)
   - Output destination: File (with specified path) or stdout (default)

3. **Additional Options**:
   - Debug flag: Enable debug output
   - User-agent: Custom user-agent for HTTP requests
   - Timeout: HTTP request timeout

The CLI follows the same error handling pattern as the library, using explicit error returns rather than exceptions for the main API. It also provides helpful error messages and a clean, intuitive interface.

## Active Decisions and Considerations

### 1. Test Case Categorization Strategy

We've decided to categorize test cases by functional area, criticality level, and test type. This provides a clear understanding of what each test case is testing and helps identify gaps in test coverage. It also allows us to prioritize test cases based on their criticality level.

### 2. Test Infrastructure Enhancement

We've decided to enhance the test infrastructure to support categorization and prioritization. This involves:

1. **Using pytest marks**: We're using pytest marks to categorize test cases by functional area, criticality level, and test type.
2. **Creating helper functions**: We've created helper functions to get test cases by category, which makes it easier to run tests by category.
3. **Creating a verification script**: We've created a script to verify that all test cases are properly implemented and categorized.

### 3. Test Case Migration Strategy

We've decided to migrate test cases from the Go implementation in order of priority:

1. **High Priority (P1)**: These test cases are essential for ensuring the Python implementation behaves the same way as the Go implementation for core functionality.
2. **Medium Priority (P2)**: These test cases are important for ensuring the Python implementation handles edge cases correctly.
3. **Low Priority (P3)**: These test cases are nice-to-have but not essential for the initial release.

### 4. Error Handling Strategy

We're following the Go implementation's pattern of using explicit error returns rather than exceptions for the main API. This makes the API more predictable and easier to use, especially for users coming from Go. However, we're adapting this pattern to be more Pythonic by using a tuple return value `(article, error)` instead of Go's multiple return values.

### 5. DOM Traversal Mapping

We're mapping Go's DOM traversal methods to BeautifulSoup's methods to ensure the content extraction algorithm works the same way in both implementations. This is a key consideration for ensuring compatibility with the Go implementation.
