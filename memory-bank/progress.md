# Progress: Python Readability

## Project Status
- **Current Phase**: Phase 6 - Testing Infrastructure
- **Overall Progress**: Completed project setup, foundation, parsing, metadata extraction, content extraction and post-processing; now implementing testing infrastructure

## What Works
- Project directory structure created
- Git repository initialized
- Memory bank documentation created
- `.gitignore` file created with Python-specific patterns
- `pyproject.toml` created with Poetry configuration
- Core dependencies added (beautifulsoup4, lxml, python-dateutil, requests)
- Development dependencies added (pytest, black, ruff)
- Formatter (black) and linter (ruff) configured
- Basic package structure created with `__init__.py` files
- `Article` dataclass defined in `models.py`
- Custom error classes defined (`ParsingError`, `ExtractionError`, `MetadataExtractionError`)
- `Readability` class created in `parser.py`
- Main entry point method `parse()` defined and implemented
- Utility functions implemented in `utils.py`
- Regular expressions and constants defined in `regexps.py`
- HTML parsing and preprocessing implemented:
  - Unwrapping images from noscript tags
  - Removing script and noscript tags
  - Preparing document for parsing (removing comments, styles, replacing br tags)
  - Extracting article title
  - Extracting metadata from meta tags and JSON-LD
  - Parsing dates
  - Getting inner text from nodes
  - Extracting favicon URL
- Core content extraction and scoring implemented:
  - Score management system using WeakKeyDictionary
  - DOM adapter methods for BeautifulSoup
  - Node initialization and classification
  - Content scoring algorithm
  - Link density calculation
  - Paragraph scoring and propagation
  - Best candidate selection
  - Article content construction
  - Multiple extraction attempts with different flags

## What's Left to Build

### Phase 1: Project Setup & Foundation
- [x] Create `.gitignore` file
- [x] Set up packaging/dependency tool (Poetry or pyproject.toml)
- [x] Add core dependencies
- [x] Configure formatter and linter
- [x] Define `Article` dataclass in `models.py` [→ Plan §2]
  <details>
  <summary>Implementation Details</summary>
  
  - Fields mirror the Go `Article` struct and `Metadata` struct combined
  - Uses appropriate Python types (`str`, `Optional[str]`, `Optional[datetime]`, etc.)
  - Includes fields: url, title, byline, content, text_content, excerpt, site_name, image, favicon, length, published_time, author, lang
  </details>
- [x] Define custom `Error` classes [→ Plan §2]
  <details>
  <summary>Implementation Details</summary>
  
  - Created base `ParsingError` class
  - Created specific error classes: `ExtractionError`, `MetadataExtractionError`
  - All inherit from `Exception`
  </details>
- [x] Create `Readability` class in `parser.py` [→ Plan §3]
  <details>
  <summary>Implementation Details</summary>
  
  - Configuration options mirror Go's `Parser` struct fields
  - Includes debug flags, thresholds, and other configuration options
  </details>
- [x] Define main entry point method `parse()` [→ Plan §3]
  <details>
  <summary>Implementation Details</summary>
  
  - Signature: `parse(self, html_content: str | bytes, url: Optional[str] = None) -> Tuple[Optional[Article], Optional[Exception]]`
  - Returns tuple of (article, error) where one is None
  - Handles exceptions internally and returns explicit error
  </details>
- [x] Stub out placeholder methods [→ Plan §3]
  <details>
  <summary>Implementation Details</summary>
  
  - Created placeholder methods: `_preprocess`, `_get_metadata`, `_grab_article`, `_postprocess_content`
  - Added method signatures with appropriate parameters and return types
  </details>
- [x] Create `utils.py` for helper functions [→ Plan §4]
  <details>
  <summary>Implementation Details</summary>
  
  - Translated helper functions from Go's `utils.go`
  - Implemented string manipulation, URL handling, and other utility functions
  </details>
- [x] Create `regexps.py` for regular expressions [→ Plan §4]
  <details>
  <summary>Implementation Details</summary>
  
  - Translated regular expressions from Go's `internal/re2go/*.re` files
  - Used `re.compile()` for performance
  - Organized by usage (preprocessing, scoring, cleaning)
  </details>

### Phase 2: Parsing & Preprocessing
- [x] Implement `parse` method to handle input HTML [→ Plan §2.1]
  <details>
  <summary>Implementation Details</summary>
  
  - Handle input `html_content` (string or bytes)
  - Use BeautifulSoup(html_content, 'lxml') for parsing
  - Handle potential parsing errors from BS4/lxml
  - Perform basic checks (e.g., does the document have a `<body>`?)
  </details>
- [x] Implement `_preprocess` method for initial HTML cleaning [→ Plan §2.2]
  <details>
  <summary>Implementation Details</summary>
  
  - Remove scripts, styles, comments (`script.decompose()`, `style.decompose()`, etc.)
  - Implement `replaceBrs` logic (find `<br>` tags and replace appropriately)
  - Implement tag conversions (e.g., `font` to `span`)
  - Ensure sequence of operations matches the Go version
  </details>

### Phase 3: Metadata Extraction
- [x] Implement `_get_metadata` method to extract article metadata [→ Plan §3.1]
  <details>
  <summary>Implementation Details</summary>
  
  - Translated Go's `getArticleMetadata` function
  - Used BeautifulSoup selectors to extract metadata
  - Extracted title, byline, excerpt, site name, published date, language
  - Populated fields in the `Article` dataclass instance
  </details>

### Phase 4: Core Content Extraction & Scoring
- [x] Implement score management system [→ Plan §4.1]
  <details>
  <summary>Implementation Details</summary>
  
  - Created `ScoreTracker` class using `weakref.WeakKeyDictionary`
  - Implemented methods to get/set/check scores for nodes
  - Avoided modifying DOM structure directly
  </details>
- [x] Implement DOM adapter methods [→ Plan §4.1]
  <details>
  <summary>Implementation Details</summary>
  
  - Created methods to map Go DOM traversal to BeautifulSoup
  - Implemented methods like `_get_element_children`, `_get_first_element_child`, etc.
  - Handled text nodes vs. element nodes appropriately
  </details>
- [x] Implement node initialization logic [→ Plan §4.1]
  <details>
  <summary>Implementation Details</summary>
  
  - Implemented `_initialize_node` method to set initial scores
  - Scored based on tag name and class/ID weight
  - Used `ScoreTracker` to store scores
  </details>
- [x] Implement scoring heuristics [→ Plan §4.2]
  <details>
  <summary>Implementation Details</summary>
  
  - Implemented `_calculate_content_score` for text-based scoring
  - Implemented `_get_class_weight` for class/ID-based scoring
  - Implemented `_get_link_density` for link density calculation
  - Implemented `_score_paragraphs` for propagating scores to ancestors
  </details>
- [x] Implement top candidate selection [→ Plan §4.3]
  <details>
  <summary>Implementation Details</summary>
  
  - Implemented `_select_best_candidate` to find highest-scored node
  - Added parent/ancestor checking for better candidates
  - Handled "only child" scenario
  </details>
- [x] Implement visibility checks [→ Plan §4.4]
  <details>
  <summary>Implementation Details</summary>
  
  - Implemented `_is_probably_visible` to check element visibility
  - Checked style attributes, hidden attribute, and aria-hidden
  - Added special case for fallback images
  </details>
- [x] Implement article construction [→ Plan §4.3]
  <details>
  <summary>Implementation Details</summary>
  
  - Implemented `_construct_article_content` to build final article
  - Added sibling content inclusion based on scores and thresholds
  - Handled special cases for paragraphs
  </details>
- [x] Implement main algorithm flow [→ Plan §4.3]
  <details>
  <summary>Implementation Details</summary>
  
  - Implemented `_grab_article` as the main extraction method
  - Added multiple extraction attempts with different flags
  - Implemented `_remove_unlikely_candidates` and `_transform_misused_divs_into_paragraphs`
  </details>

### Phase 5: Post-processing & Output Generation
- [x] Implement content cleaning [→ Plan §5.1]
  <details>
  <summary>Implementation Details</summary>
  
  - Implemented `_clean_styles` to remove presentational attributes
  - Implemented `_clean_classes` to remove class attributes
  - Implemented `_clean_conditionally` for conditional element removal
  - Implemented `_clean_headers` for header cleaning
  </details>
- [x] Implement link fixing [→ Plan §5.1]
  <details>
  <summary>Implementation Details</summary>
  
  - Implemented `_fix_relative_uris` to make links absolute
  - Handled different types of media elements (img, video, etc.)
  - Processed srcset attributes correctly
  </details>
- [x] Implement final article preparation [→ Plan §5.2]
  <details>
  <summary>Implementation Details</summary>
  
  - Implemented `_prepare_article` for final cleanup
  - Added `_remove_empty_nodes` to clean empty elements
  - Added `_ensure_paragraph_structure` for proper paragraph structure
  </details>
- [x] Implement post-processing [→ Plan §5.3]
  <details>
  <summary>Implementation Details</summary>
  
  - Implemented `_postprocess_content` to orchestrate all cleanup steps
  - Integrated all cleaning methods in the right order
  - Added readability attribute cleanup
  </details>

### Phase 6: Testing Infrastructure
- [ ] Configure pytest [→ Plan §6.1]
  <details>
  <summary>Implementation Details</summary>
  
  - Set up pytest configuration
  - Copy test-pages directory from Go project
  </details>
- [ ] Create test loader [→ Plan §6.2]
  <details>
  <summary>Implementation Details</summary>
  
  - Write functions to discover test case directories
  - Load source.html, expected.html, and expected-metadata.json
  </details>
- [ ] Implement test cases [→ Plan §6.3]
  <details>
  <summary>Implementation Details</summary>
  
  - Use pytest.mark.parametrize for test cases
  - Instantiate Readability and call parse()
  - Compare results with expected output
  </details>
- [ ] Run and debug tests [→ Plan §6.4]
  <details>
  <summary>Implementation Details</summary>
  
  - Run tests frequently during development
  - Debug failures by comparing with Go implementation
  </details>

### Phase 7: CLI Implementation
- [ ] Choose CLI framework [→ Plan §7.1]
  <details>
  <summary>Implementation Details</summary>
  
  - Evaluate argparse, click, or typer
  - Select based on project needs
  </details>
- [ ] Define CLI arguments [→ Plan §7.2]
  <details>
  <summary>Implementation Details</summary>
  
  - Input file/URL
  - Output file
  - Output format (HTML/JSON)
  - Debug/verbosity flags
  </details>
- [ ] Implement CLI logic [→ Plan §7.3]
  <details>
  <summary>Implementation Details</summary>
  
  - Parse arguments
  - Handle URL or file input
  - Call Readability.parse()
  - Format and output results
  </details>
- [ ] Define entry point [→ Plan §7.4]
  <details>
  <summary>Implementation Details</summary>
  
  - Define entry point in pyproject.toml
  </details>

### Phase 8: Documentation & Packaging
- [ ] Write README.md [→ Plan §8.1]
  <details>
  <summary>Implementation Details</summary>
  
  - Cover installation, usage examples, CLI usage
  - Compare with upstream, note differences
  </details>
- [ ] Add docstrings [→ Plan §8.2]
  <details>
  <summary>Implementation Details</summary>
  
  - Add comprehensive docstrings (PEP 257)
  - Document all classes, methods, and functions
  </details>
- [ ] Finalize packaging [→ Plan §8.3]
  <details>
  <summary>Implementation Details</summary>
  
  - Finalize pyproject.toml
  - Build distributions
  </details>
- [ ] Optional: Publish to PyPI [→ Plan §8.4]
  <details>
  <summary>Implementation Details</summary>
  
  - Create PyPI account if needed
  - Upload package to PyPI
  </details>

## Implementation Notes

### Phase 1: Project Setup & Foundation
- Chose Poetry over pip/setuptools for better dependency management and virtual environment integration
- Used ruff over flake8 for faster linting performance and more comprehensive rule set
- Implemented `Article` dataclass with all fields from Go implementation plus `url` field for convenience
- Created a hierarchy of error classes to allow for more specific error handling
- Organized regular expressions in `regexps.py` to match the structure of the Go implementation

### Phase 2: Parsing & Preprocessing (Completed)
- Used BeautifulSoup's encoding detection for handling bytes input
- Mapped Go's DOM traversal methods to BeautifulSoup equivalents
- Implemented HTML preprocessing including comment removal, style removal, and BR tag handling
- Extracted article title using similar heuristics as the Go implementation
- Implemented JSON-LD metadata extraction for article information

### Phase 3: Metadata Extraction (Completed)
- Implemented metadata extraction from meta tags and JSON-LD
- Extracted title, byline, excerpt, site name, published date, and language
- Used HTML unescape to handle HTML entities in metadata
- Implemented date parsing using python-dateutil

### Phase 4: Core Content Extraction & Scoring (Completed)
- Implemented score management using `ScoreTracker` class with `weakref.WeakKeyDictionary`
- Created DOM adapter methods to map Go DOM traversal to BeautifulSoup
- Implemented node initialization and classification based on tag names and class/ID
- Implemented content scoring algorithm based on text characteristics and link density
- Implemented paragraph scoring with score propagation to ancestors
- Implemented best candidate selection with parent/ancestor checking
- Implemented article construction with sibling content inclusion
- Implemented multiple extraction attempts with different flags for robustness

### Phase 5: Post-processing & Output Generation (Completed)
- Implemented style cleaning to remove presentational attributes
- Implemented class cleaning with preservation of specified classes
- Implemented conditional cleaning for forms, tables, and divs
- Implemented header cleaning based on class weight and link density
- Implemented link fixing to make all URLs absolute
- Implemented final article preparation with empty node removal and paragraph structure

## Technical Debt
- Need to ensure proper memory management when dealing with large HTML documents
- Consider optimizing regular expression usage for performance
- May need to revisit the scoring algorithm implementation for better performance
- Consider adding more comprehensive error handling for edge cases

## Known Issues
- No implementation issues yet, but need to verify against test cases

## Milestones
- [x] Project initialized
- [x] Core data structures implemented
- [x] Main class structure implemented
- [x] Parsing and preprocessing implemented
- [x] Metadata extraction implemented
- [x] Content extraction and scoring implemented
- [x] Post-processing implemented
- [ ] Tests passing
- [ ] CLI implemented
- [ ] Documentation completed
- [ ] Package ready for distribution

## Next Immediate Tasks
1. Install Poetry and set up virtual environment
2. Set up pytest and configure test infrastructure
3. Implement test cases and compare with Go implementation
4. Implement CLI interface
5. Complete documentation and packaging
