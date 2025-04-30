# Test Case Categorization for Python Readability

## Overview

This document provides a comprehensive categorization of test cases for the Python Readability project. It categorizes test cases by functional area, criticality level, and test type to provide a clear understanding of what each test case is testing and to identify gaps in test coverage.

## Categorization Framework

### Functional Areas

- **HTML Parsing**: Tests for parsing HTML documents
- **Metadata Extraction**: Tests for extracting metadata (title, author, date, etc.)
- **Content Identification**: Tests for identifying the main content of a page
- **Content Cleaning**: Tests for cleaning and formatting the extracted content
- **URL Handling**: Tests for handling and resolving URLs
- **Visibility Detection**: Tests for detecting and handling hidden elements
- **Text Normalization**: Tests for normalizing text (whitespace, entities, etc.)
- **Real-world Websites**: Tests using actual website content

### Criticality Levels

- **P0 (Critical)**: Tests core functionality that must work for the library to be usable
- **P1 (High)**: Tests important features that most users will rely on
- **P2 (Medium)**: Tests secondary features or edge cases
- **P3 (Low)**: Tests nice-to-have features or very rare edge cases

### Test Types

- **Basic**: Simple test cases that verify fundamental functionality
- **Feature**: Tests specific features of the library
- **Edge Case**: Tests unusual or challenging inputs
- **Real-world**: Tests using actual website content

## Test Case Inventory

### Python Implementation Test Cases

| Test Case | Functional Area | Criticality | Test Type | Description | Status |
|-----------|----------------|------------|-----------|-------------|--------|
| 001 | Content Identification | P0 | Basic | Basic article extraction with code blocks and formatting | Implemented |
| 002 | Content Identification | P0 | Basic | Basic article extraction with simple content | Implemented |
| 003-metadata-preferred | Metadata Extraction | P1 | Feature | Tests preference for metadata in meta tags | Implemented |
| 004-metadata-space-separated-properties | Metadata Extraction | P1 | Feature | Tests handling of space-separated properties in metadata | Implemented |
| base-url | URL Handling | P1 | Feature | Tests conversion of relative URLs to absolute URLs | Implemented |
| basic-tags-cleaning | Content Cleaning | P1 | Feature | Tests cleaning of basic HTML tags | Implemented |
| comment-inside-script-parsing | HTML Parsing | P2 | Edge Case | Tests handling of comments inside script tags | Implemented |
| hidden-nodes | Visibility Detection | P0 | Feature | Tests exclusion of hidden elements | Implemented |
| keep-images | Content Cleaning | P1 | Feature | Tests preservation of image elements in content | Implemented |
| medium-1 | Real-world Websites | P0 | Real-world | Tests extraction from Medium article | Implemented |
| metadata-content-missing | Metadata Extraction | P1 | Edge Case | Tests handling of missing metadata | Implemented |
| missing-paragraphs | Content Cleaning | P1 | Edge Case | Tests handling of content without proper paragraph tags | Implemented |
| mozilla-1 | Real-world Websites | P0 | Real-world | Tests extraction from Mozilla documentation | Implemented |
| normalize-spaces | Text Normalization | P1 | Feature | Tests normalization of whitespace in content | Implemented |
| nytimes-1 | Real-world Websites | P0 | Real-world | Tests extraction from New York Times article | Implemented |
| remove-script-tags | Content Cleaning | P0 | Feature | Tests removal of script tags from content | Implemented |
| replace-brs | Content Cleaning | P1 | Feature | Tests replacement of BR tags with paragraph breaks | Implemented |
| svg-parsing | HTML Parsing | P2 | Edge Case | Tests handling of SVG elements in content | Implemented |
| wikipedia | Real-world Websites | P0 | Real-world | Tests extraction from Wikipedia article | Implemented |

### Go Implementation Test Cases (Not Yet Migrated)

| Test Case | Functional Area | Criticality | Test Type | Description | Status |
|-----------|----------------|------------|-----------|-------------|--------|
| base-url-base-element | URL Handling | P1 | Feature | Tests handling of base element for URL resolution | Not Implemented |
| base-url-base-element-relative | URL Handling | P1 | Feature | Tests handling of relative URLs in base element | Not Implemented |
| ehow-2 | Real-world Websites | P2 | Real-world | Tests extraction from eHow article | Not Implemented |
| herald-sun-1 | Real-world Websites | P2 | Real-world | Tests extraction from Herald Sun article | Not Implemented |
| js-link-replacement | Content Cleaning | P2 | Feature | Tests handling of JavaScript links | Not Implemented |
| medium-2 | Real-world Websites | P1 | Real-world | Tests extraction from another Medium article | Not Implemented |
| qq | Text Normalization | P2 | Edge Case | Tests handling of non-Latin character sets | Not Implemented |
| remove-aria-hidden | Visibility Detection | P1 | Feature | Tests handling of aria-hidden attribute | Not Implemented |
| replace-font-tags | Content Cleaning | P1 | Feature | Tests replacement of font tags with span tags | Not Implemented |
| rtl-3 | Text Normalization | P2 | Edge Case | Tests handling of right-to-left text | Not Implemented |
| rtl-4 | Text Normalization | P2 | Edge Case | Tests handling of right-to-left text | Not Implemented |

## Test Case Details

### 001

**Functional Area**: Content Identification  
**Criticality**: P0  
**Test Type**: Basic  
**Description**: Tests basic article extraction with code blocks and formatting.  
**What it Tests**:
- Extraction of main article content
- Preservation of code blocks and pre-formatted text
- Handling of formatting elements (strong, em)
- Handling of links and images
- Extraction of metadata (title, byline, excerpt)
- Handling of blockquotes

### 002

**Functional Area**: Content Identification  
**Criticality**: P0  
**Test Type**: Basic  
**Description**: Tests basic article extraction with simple content.  
**What it Tests**:
- Extraction of main article content
- Basic metadata extraction

### 003-metadata-preferred

**Functional Area**: Metadata Extraction  
**Criticality**: P1  
**Test Type**: Feature  
**Description**: Tests preference for metadata in meta tags.  
**What it Tests**:
- Extraction of metadata from meta tags
- Preference order for metadata sources

### 004-metadata-space-separated-properties

**Functional Area**: Metadata Extraction  
**Criticality**: P1  
**Test Type**: Feature  
**Description**: Tests handling of space-separated properties in metadata.  
**What it Tests**:
- Parsing of space-separated property values in meta tags

### base-url

**Functional Area**: URL Handling  
**Criticality**: P1  
**Test Type**: Feature  
**Description**: Tests conversion of relative URLs to absolute URLs.  
**What it Tests**:
- Conversion of relative URLs to absolute URLs
- Handling of different URL formats (relative, absolute, fragment)
- URL resolution for links and images

### basic-tags-cleaning

**Functional Area**: Content Cleaning  
**Criticality**: P1  
**Test Type**: Feature  
**Description**: Tests cleaning of basic HTML tags.  
**What it Tests**:
- Removal of unnecessary tags
- Preservation of important content tags

### comment-inside-script-parsing

**Functional Area**: HTML Parsing  
**Criticality**: P2  
**Test Type**: Edge Case  
**Description**: Tests handling of comments inside script tags.  
**What it Tests**:
- Proper parsing and removal of script tags containing comments
- Prevention of comment leakage into content

### hidden-nodes

**Functional Area**: Visibility Detection  
**Criticality**: P0  
**Test Type**: Feature  
**Description**: Tests exclusion of hidden elements.  
**What it Tests**:
- Exclusion of elements with style="display: none;"
- Exclusion of elements with hidden="hidden" attribute
- Exclusion of H1 elements (used for title)
- Preservation of visible content

### keep-images

**Functional Area**: Content Cleaning  
**Criticality**: P1  
**Test Type**: Feature  
**Description**: Tests preservation of image elements in content.  
**What it Tests**:
- Preservation of image elements in the extracted content
- Proper handling of image attributes

### medium-1

**Functional Area**: Real-world Websites  
**Criticality**: P0  
**Test Type**: Real-world  
**Description**: Tests extraction from Medium article.  
**What it Tests**:
- Extraction from a real Medium article
- Handling of Medium's specific HTML structure

### metadata-content-missing

**Functional Area**: Metadata Extraction  
**Criticality**: P1  
**Test Type**: Edge Case  
**Description**: Tests handling of missing metadata.  
**What it Tests**:
- Graceful handling of missing metadata
- Fallback strategies for metadata extraction

### missing-paragraphs

**Functional Area**: Content Cleaning  
**Criticality**: P1  
**Test Type**: Edge Case  
**Description**: Tests handling of content without proper paragraph tags.  
**What it Tests**:
- Handling of content without proper paragraph tags
- Preservation of content structure
- Exclusion of H1 elements (used for title)

### mozilla-1

**Functional Area**: Real-world Websites  
**Criticality**: P0  
**Test Type**: Real-world  
**Description**: Tests extraction from Mozilla documentation.  
**What it Tests**:
- Extraction from Mozilla documentation
- Handling of technical documentation structure

### normalize-spaces

**Functional Area**: Text Normalization  
**Criticality**: P1  
**Test Type**: Feature  
**Description**: Tests normalization of whitespace in content.  
**What it Tests**:
- Normalization of whitespace (spaces, tabs, newlines)
- Preservation of whitespace in pre-formatted content
- Handling of excessive whitespace

### nytimes-1

**Functional Area**: Real-world Websites  
**Criticality**: P0  
**Test Type**: Real-world  
**Description**: Tests extraction from New York Times article.  
**What it Tests**:
- Extraction from a New York Times article
- Handling of news article structure

### remove-script-tags

**Functional Area**: Content Cleaning  
**Criticality**: P0  
**Test Type**: Feature  
**Description**: Tests removal of script tags from content.  
**What it Tests**:
- Removal of script tags from content
- Prevention of script execution

### replace-brs

**Functional Area**: Content Cleaning  
**Criticality**: P1  
**Test Type**: Feature  
**Description**: Tests replacement of BR tags with paragraph breaks.  
**What it Tests**:
- Replacement of BR tags with paragraph breaks
- Handling of consecutive BR tags

### svg-parsing

**Functional Area**: HTML Parsing  
**Criticality**: P2  
**Test Type**: Edge Case  
**Description**: Tests handling of SVG elements in content.  
**What it Tests**:
- Parsing of SVG elements
- Preservation or removal of SVG content

### wikipedia

**Functional Area**: Real-world Websites  
**Criticality**: P0  
**Test Type**: Real-world  
**Description**: Tests extraction from Wikipedia article.  
**What it Tests**:
- Extraction from a Wikipedia article
- Handling of Wikipedia's specific HTML structure

## Coverage Analysis

### Coverage by Functional Area

| Functional Area | P0 | P1 | P2 | P3 | Total |
|----------------|----|----|----|----|-------|
| HTML Parsing | 0 | 0 | 2 | 0 | 2 |
| Metadata Extraction | 0 | 3 | 0 | 0 | 3 |
| Content Identification | 2 | 0 | 0 | 0 | 2 |
| Content Cleaning | 1 | 3 | 0 | 0 | 4 |
| URL Handling | 0 | 1 | 0 | 0 | 1 |
| Visibility Detection | 1 | 0 | 0 | 0 | 1 |
| Text Normalization | 0 | 1 | 0 | 0 | 1 |
| Real-world Websites | 4 | 0 | 0 | 0 | 4 |
| **Total** | **8** | **8** | **2** | **0** | **18** |

### Coverage by Test Type

| Test Type | Count | Percentage |
|-----------|-------|------------|
| Basic | 2 | 11% |
| Feature | 9 | 50% |
| Edge Case | 3 | 17% |
| Real-world | 4 | 22% |

### Identified Gaps

1. **URL Handling**: 
   - Missing tests for base element handling
   - Limited tests for URL resolution edge cases

2. **Visibility Detection**:
   - Limited tests for aria-hidden attributes
   - No tests for CSS visibility properties

3. **Text Normalization**:
   - Missing tests for right-to-left text
   - Missing tests for non-Latin character sets
   - Limited tests for HTML entity normalization

4. **HTML Parsing**:
   - Limited tests for malformed HTML
   - No tests for HTML5 specific elements

5. **Content Cleaning**:
   - No tests for table handling
   - Limited tests for form element removal
   - No tests for iframe handling

6. **Metadata Extraction**:
   - Limited tests for schema.org metadata
   - No tests for Open Graph protocol
   - No tests for Twitter Card metadata

## Recommendations

### Test Cases to Migrate from Go Implementation

1. **High Priority (P1)**:
   - base-url-base-element
   - base-url-base-element-relative
   - remove-aria-hidden
   - replace-font-tags
   - medium-2

2. **Medium Priority (P2)**:
   - rtl-3
   - rtl-4
   - qq
   - js-link-replacement
   - ehow-2
   - herald-sun-1

### New Test Cases to Create

1. **HTML Parsing**:
   - malformed-html (P2): Test handling of malformed HTML
   - html5-elements (P2): Test handling of HTML5 specific elements

2. **Content Cleaning**:
   - table-handling (P1): Test handling of table elements
   - form-removal (P1): Test removal of form elements
   - iframe-handling (P2): Test handling of iframe elements

3. **Metadata Extraction**:
   - schema-org (P1): Test extraction of schema.org metadata
   - open-graph (P1): Test extraction of Open Graph protocol metadata
   - twitter-card (P2): Test extraction of Twitter Card metadata

4. **Visibility Detection**:
   - css-visibility (P1): Test handling of CSS visibility properties

## Implementation Priorities

### First Wave: Critical Functionality (P0)

1. **Content Identification**: 001, 002
2. **Visibility Detection**: hidden-nodes
3. **Content Cleaning**: remove-script-tags
4. **Real-world Websites**: nytimes-1, wikipedia, mozilla-1, medium-1

### Second Wave: High Priority Features (P1)

1. **Metadata Extraction**: 003-metadata-preferred, 004-metadata-space-separated-properties, metadata-content-missing
2. **URL Handling**: base-url, base-url-base-element, base-url-base-element-relative
3. **Content Cleaning**: keep-images, replace-brs, basic-tags-cleaning
4. **Text Normalization**: normalize-spaces
5. **Visibility Detection**: remove-aria-hidden (to migrate)

### Third Wave: Medium Priority Features (P2)

1. **HTML Parsing**: svg-parsing, comment-inside-script-parsing
2. **Text Normalization**: rtl-3, rtl-4, qq (to migrate)
3. **Content Cleaning**: js-link-replacement (to migrate)
4. **Real-world Websites**: ehow-2, herald-sun-1 (to migrate)

## Next Steps

1. **Migrate High Priority Test Cases**: Use the test-case-migration-script.py to migrate the high-priority test cases from the Go implementation.
2. **Update Test Infrastructure**: Modify the test infrastructure to support categorization and prioritization.
3. **Create New Test Cases**: Create new test cases to fill the identified gaps.
4. **Run Comprehensive Tests**: Run tests for each category to verify functionality.
