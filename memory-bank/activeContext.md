# Active Context: Python Readability

## Current Work Focus
The project has completed the initial setup phase (Phase 1), parsing and preprocessing (Phase 2), metadata extraction (Phase 3), core content extraction and scoring (Phase 4), and post-processing (Phase 5). We're now working on Phase 6: Testing Infrastructure to verify the implementation against the original Go version.

## Recent Changes
- Created project directory structure (`python-readability/`, `readability/`, `tests/`, `cli/`)
- Initialized Git repository
- Created memory bank documentation to track project progress and context
- Created `.gitignore` file with Python-specific patterns
- Created `pyproject.toml` with Poetry configuration, dependencies, and development tools
- Created basic package structure with `__init__.py` files in `readability/`, `cli/`, and `tests/` directories
- Created `readability/models.py` with `Article` dataclass and custom error classes
- Created `readability/parser.py` with `Readability` class and implemented core methods
- Created `readability/utils.py` with utility functions
- Created `readability/regexps.py` with regular expressions and constants
- Implemented HTML parsing and preprocessing functionality
- Implemented metadata extraction from meta tags and JSON-LD
- Implemented core content extraction and scoring algorithm
- Implemented post-processing and output generation
- Updated project documentation to reflect current progress

## Next Steps
1. **Complete Project Setup**:
   - Install Poetry and set up virtual environment

2. **Phase 1: Project Setup & Foundation** ✓
   - ✓ Create `readability/models.py` with `Article` dataclass
   - ✓ Define custom `Error` classes
   - ✓ Create `readability/parser.py` with `Readability` class
   - ✓ Define main entry point method `parse()`
   - ✓ Stub out placeholder methods for major steps
   - ✓ Create `readability/utils.py` for helper functions
   - ✓ Create `readability/regexps.py` for regular expressions

3. **Phase 2: Parsing & Preprocessing** ✓
   - ✓ Implement `parse` method to handle input HTML
   - ✓ Implement `_preprocess` method for initial HTML cleaning

4. **Phase 3: Metadata Extraction** ✓
   - ✓ Implement `_get_metadata` method to extract article metadata
   - ✓ Implement `_get_json_ld` method to extract metadata from JSON-LD
   - ✓ Implement `_get_article_title` method to extract article title
   - ✓ Implement `_get_article_favicon` method to extract favicon URL

5. **Phase 4: Core Content Extraction & Scoring** ✓
   - ✓ Implement score management system
     - Created `ScoreTracker` class using `weakref.WeakKeyDictionary`
     - Added methods to get/set/check scores for nodes
   - ✓ Implement DOM adapter methods
     - Created helper methods for consistent DOM traversal
     - Mapped Go DOM methods to BeautifulSoup equivalents
   - ✓ Implement node classification and initialization
     - Added class weight calculation
     - Initialized nodes with baseline scores
     - Added visibility detection
   - ✓ Implement content scoring logic
     - Calculated link density
     - Scored paragraphs based on content
     - Propagated scores to ancestor nodes
   - ✓ Implement candidate selection
     - Selected best candidate based on scores
     - Included related content from siblings
   - ✓ Implement main algorithm flow
     - Removed unlikely candidates
     - Transformed misused divs into paragraphs
     - Orchestrated the extraction process

6. **Phase 5: Post-processing & Output Generation** ✓
   - ✓ Implement content cleaning
     - Removed presentational attributes
     - Cleaned class attributes
     - Implemented conditional element removal
   - ✓ Implement link fixing
     - Made links absolute using base URL
     - Handled different media elements
     - Processed srcset attributes
   - ✓ Implement final article preparation
     - Removed empty nodes
     - Ensured proper paragraph structure
     - Cleaned up readability attributes

7. **Phase 6: Testing Infrastructure** (Current Focus)
   - Configure pytest
     - Set up pytest configuration
     - Copy test-pages directory from Go project
   - Create test loader
     - Write functions to discover test case directories
     - Load source.html, expected.html, and expected-metadata.json
   - Implement test cases
     - Use pytest.mark.parametrize for test cases
     - Compare results with expected output
   - Run and debug tests
     - Run tests frequently during development
     - Debug failures by comparing with Go implementation

## Active Decisions and Considerations

### Implementation Strategy
- Following a phased approach as outlined in the project plan
- Focusing on setting up the project structure and core components first
- Planning to implement the parsing logic in a step-by-step manner, following the Go implementation closely

### Key Questions
- How closely should we follow the Go implementation's structure vs. making it more Pythonic?
- Should we implement the CLI interface early or focus on the core library first?

### Current Challenges
- Setting up comprehensive test infrastructure to verify implementation against Go version
- Handling differences in HTML output formatting between Go and Python implementations
- Creating robust comparison methods for HTML and metadata
- Dealing with potential edge cases in test pages
- Ensuring test coverage for all implemented functionality
- Debugging any discrepancies between Python implementation and Go implementation results

## Reference Materials
- Original Go implementation in `go-readability/` directory
- Project plan in `project-plan.md`
- Test cases in `go-readability/test-pages/`

## Document Integration
The project uses two complementary documents to track implementation:

1. **project-plan.md**: The detailed implementation roadmap with specific technical guidance
   - Provides step-by-step instructions for each phase
   - Includes implementation details and approaches
   - Now includes status tracking with completion dates

2. **memory-bank/progress.md**: The progress tracking document
   - Tracks task completion status
   - Includes collapsible implementation details
   - Contains references to corresponding sections in project-plan.md
   - Includes implementation notes and technical debt tracking

These documents are now integrated with:
- Consistent phase and task naming
- Cross-references between documents (e.g., [→ Plan §2.1])
- Shared status tracking
- Complementary information (plan has "how to implement", progress has "what has been implemented")
