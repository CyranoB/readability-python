Here is a detailed implementation plan for porting Mozilla Readability to Python using the `go-readability` as example. This plan assumes we are aiming for high fidelity and leveraging Python best practices (`dataclasses`, standard tooling).
The goal of this project is to implement a python version of the go-readability project.


**Phase 1: Project Setup & Foundation (Pythonic Base)** [COMPLETED: 4/28/2025]

1.  **Environment & Tooling:** [COMPLETED: 4/28/2025]
    * [X] Create project directory: `python-readability/`
    * [X] Set up subdirectories: `readability/` (library code), `tests/`, `cli/` (optional, for CLI code).
    * [X] Initialize Git: `git init`
    * [X] Choose and set up packaging/dependency tool: `poetry init` or create `pyproject.toml` manually.
    * [X] Add core dependencies: `beautifulsoup4`, `lxml`, `python-dateutil`, `requests` (for CLI/fetching), `pytest` (for testing).
    * [X] Configure formatter (`black`) and linter (`ruff` or `flake8`) via `pyproject.toml`.
2.  **Core Data Structures (`readability/models.py`):** [COMPLETED: 4/28/2025]
    * [X] Define an `Article` dataclass. Fields should mirror the Go `Article` struct and `Metadata` struct combined (e.g., `url`, `title`, `byline`, `content` (HTML string), `text_content` (plain text), `excerpt`, `site_name`, `image`, `favicon`, `length` (char count), `published_time` (datetime object), `author`, `lang`). Use appropriate Python types (`str`, `Optional[str]`, `Optional[datetime]`, etc.).
    * [X] Define custom `Error` classes (inheriting from `Exception`) for different failure modes if needed (e.g., `ParsingError`, `ExtractionError`).
3.  **Main Class Structure (`readability/parser.py`):** [COMPLETED: 4/28/2025]
    * [X] Define the main `Readability` class. Its `__init__` might take configuration options mirroring Go's `Parser` struct fields if needed (e.g., debug flags, specific thresholds).
    * [X] Define the main entry point method: `parse(self, html_content: str | bytes, url: Optional[str] = None) -> Tuple[Optional[Article], Optional[Exception]]`. This method will orchestrate the parsing process and adhere to the "explicit error return" decision. Internally, it can use exceptions, but it should catch them and return the `(None, error)` tuple. On success, it returns `(article, None)`.
    * [X] Stub out placeholder methods corresponding to major steps in the Go version (e.g., `_preprocess`, `_get_metadata`, `_grab_article`, `_postprocess_content`).
4.  **Utilities & Regexps (`readability/utils.py`, `readability/regexps.py`):** [COMPLETED: 4/28/2025]
    * [X] Create `utils.py` for helper functions translated from Go's `utils.go` or new Python-specific helpers (e.g., advanced whitespace normalization).
    * [X] Create `regexps.py`. Translate all regular expressions from Go's `internal/re2go/*.re` files into Python's `re` syntax. Use `re.compile()` for performance and organize them clearly (e.g., grouping by usage like `PREPROCESSING_REGEXPS`, `SCORING_REGEXPS`, `CLEANING_REGEXPS`).

**Phase 2: Parsing & Preprocessing (Getting the Raw Material)** [COMPLETED: 4/28/2025]

1.  **Initial Parse (`Readability.parse` method):** [COMPLETED: 4/28/2025]
    * [X] Handle input `html_content` (string or bytes). If bytes, let BeautifulSoup/lxml handle encoding detection. Consider using `requests` library's encoding detection if fetching URLs directly later.
    * [X] Parse using `BeautifulSoup(html_content, 'lxml')`. Handle potential parsing errors from BS4/lxml.
    * [X] Perform basic checks (e.g., does the document have a `<body>`?).
2.  **Preprocessing (`Readability._preprocess` method):** [COMPLETED: 4/28/2025]
    * [X] Translate Go's `preprocess` steps meticulously using BeautifulSoup methods:
        * Remove scripts, styles, comments (`script.decompose()`, `style.decompose()`, etc.).
        * Implement `replaceBrs` logic (find `<br>` tags and replace appropriately).
        * Implement tag conversions (e.g., `font` to `span`) if present in the Go logic.
        * Ensure the sequence of operations matches the Go version.

**Phase 3: Metadata Extraction (Finding Title, Author, etc.)** [COMPLETED: 4/28/2025]

1.  **Implement Metadata Logic (`Readability._get_metadata` method):** [COMPLETED: 4/28/2025]
    * [X] Translate Go's `getArticleMetadata` function.
    * [X] Use BeautifulSoup selectors (`soup.select_one(...)`, `soup.find(...)`) and heuristics from the Go code to extract:
        * Title (multiple potential sources like `<title>`, `og:title`, `<h1>`).
        * Byline/Author.
        * Excerpt/Description (`og:description`, meta description).
        * Site Name (`og:site_name`).
        * Published Date (use `python-dateutil.parser.parse` on candidate strings).
        * Language (check `<html>` lang attribute).
    * [X] Populate the corresponding fields in the `Article` dataclass instance being built.

**Phase 4: Core Content Extraction & Scoring (The Heart of Readability)** [COMPLETED: 4/28/2025]

1.  **Node Initialization (`Readability._initialize_node` helper):** [COMPLETED: 4/28/2025]
    * [X] Traverse the relevant part of the parsed document (usually starting from `<body>`).
    * [X] Attach initial scoring information to nodes. Use BeautifulSoup's ability to add custom attributes (`tag['readability_score'] = 0`) or maintain a separate `dict` mapping nodes to scores.
2.  **Scoring Heuristics (`Readability._calculate_content_score`, `_get_node_weight` helpers):** [COMPLETED: 4/28/2025]
    * [X] **Crucial Step:** Carefully translate the Go functions responsible for scoring nodes (`calculateContentScore`, `getNodeWeight`).
    * [X] Map Go DOM traversal (`dom.FirstElementChild`, etc.) to BeautifulSoup equivalents (`.children`, `.parent`, `.find_next_sibling()`, `.find_previous_sibling()` etc.). Be mindful of differences (e.g., BS4 iterators vs direct properties).
    * [X] Apply scoring based on tag names, classes/IDs (using regexps from `regexps.py`), text content length, link density, depth, etc.
    * [X] Implement score propagation logic (parents gaining score from children).
3.  **Top Candidate Selection (`Readability._grab_article` method):** [COMPLETED: 4/28/2025]
    * [X] Translate Go's `grabArticle` logic.
    * [X] Find the node(s) with the highest score.
    * [X] Implement logic to check sibling nodes and potentially merge them if scores are close.
    * [X] This method should return the top candidate node (a BS4 `Tag` object).
4.  **Visibility Checks (`Readability._is_probably_visible` helper):** [COMPLETED: 4/28/2025]
    * [X] Translate Go's `isProbablyVisible` function. Check element styles (`style` attribute) and classes/IDs associated with hidden elements.

**Phase 5: Post-processing & Output Generation (Cleaning Up)** [COMPLETED: 4/28/2025]

1.  **Content Cleaning (`Readability._postprocess_content` method):** [COMPLETED: 4/28/2025]
    * [X] Takes the top candidate node as input.
    * [X] Translate Go's `postProcessContent` logic:
        * Remove unlikely nodes based on class/ID regexps.
        * Clean attributes (remove excessive styling, event handlers).
        * Make links absolute (using `urllib.parse.urljoin` with the base URL).
        * Implement conditional cleaning (`cleanConditionally` logic).
        * Handle tables (cleaning or preserving).
        * Remove temporary Readability attributes added during scoring.
2.  **HTML & Text Generation:** [COMPLETED: 4/28/2025]
    * [X] Serialize the cleaned content node back to an HTML string (e.g., `top_node.prettify()` or `str(top_node)`). Store in `Article.content`.
    * [X] Extract plain text from the cleaned node (`top_node.get_text(separator=' ', strip=True)`). Store in `Article.text_content`.
    * [X] Calculate final length (`len(Article.text_content)`). Store in `Article.length`.
3.  **Final Return (`Readability.parse`):** [COMPLETED: 4/28/2025] Return the completed `(article, None)`.

**Phase 6: Testing Infrastructure (`tests/`)** [COMPLETED: 4/29/2025]

1.  **Setup:** [COMPLETED: 4/29/2025] Configure `pytest`. Copy the `test-pages/` directory from the Go project into the `tests/` directory.
2.  **Test Loader (`tests/conftest.py` or helpers):** [COMPLETED: 4/29/2025]
    * [X] Write functions to automatically discover all test case directories inside `tests/test-pages/`.
    * [X] For each case, load `source.html`, `expected.html`, and `expected-metadata.json`.
3.  **Test Implementation (`tests/test_readability.py`):** [COMPLETED: 4/29/2025]
    * [X] Use `pytest.mark.parametrize` to create tests for each discovered test case.
    * [X] Inside the test function:
        * Instantiate `Readability`.
        * Call `readability.parse(source_html_content, url=case_url)`. Assert no error was returned.
        * Compare `Article` fields against loaded `expected-metadata.json` (use helpers for date/numeric comparisons).
        * Compare the generated `Article.content` HTML with `expected.html`. Start with normalized string comparison; consider semantic (tree) comparison if needed for robustness.
4.  **Iteration:** [COMPLETED: 4/29/2025] Run `pytest` frequently. Debug failures by comparing Python code execution flow and intermediate values against the Go version's logic for the failing test case.
5.  **Project Reorganization:** [COMPLETED: 4/29/2025]
    * [X] Create directory structure for better organization:
        * `tests/docs/` for test documentation
        * `tests/scripts/` for test utility scripts
        * `tests/fixtures/` for test fixtures
    * [X] Move test-related files to appropriate directories
    * [X] Update path references in scripts to reflect new directory structure

**Phase 7: CLI Implementation (`cli/`)** [COMPLETED: 4/29/2025]

1.  **Framework:** [COMPLETED: 4/29/2025] Choose `argparse` (built-in) or `click`/`typer`. (Selected `argparse`)
2.  **Arguments:** [COMPLETED: 4/29/2025] Define CLI arguments (input file/URL, output file, output format (HTML/JSON), debug/verbosity flags).
3.  **Logic (`cli/main.py`):** [COMPLETED: 4/29/2025]
    * [X] Parse arguments.
    * [X] If URL input, use `requests.get()` to fetch content (handle errors). If file input, read the file.
    * [X] Instantiate `Readability`.
    * [X] Call `readability.parse()`.
    * [X] Check the returned `(result, error)`. Print error to `stderr` and exit if error.
    * [X] Format the `Article` object (e.g., print content HTML, or dump metadata as JSON) based on flags. Print to `stdout` or output file.
4.  **Entry Point:** [COMPLETED: 4/29/2025] Define entry point in `pyproject.toml` for the CLI script.

**Phase 8: Documentation & Packaging** [COMPLETED: 4/29/2025]

1.  **README:** [COMPLETED: 4/29/2025] Write `README.md` covering installation, library usage examples, CLI usage, comparison to upstream, known differences (if any).
2.  **Docstrings:** [COMPLETED: 4/29/2025] Add comprehensive docstrings (PEP 257) to all classes, methods, and functions.
3.  **Packaging:** [COMPLETED: 4/29/2025] Finalize `pyproject.toml`, build distributions (`python -m build`).
   * [X] Enhanced metadata in pyproject.toml
   * [X] Created setup.py for pip installation
   * [X] Added MANIFEST.in for source distribution
   * [X] Created publishing script and documentation
4.  **Optional:** [PREPARED: 4/29/2025] Publish to PyPI.
   * [X] Created publishing script with TestPyPI support
   * [X] Added detailed instructions in PACKAGING.md

This plan provides a detailed roadmap. The most challenging parts will be the meticulous translation of scoring (Phase 4) and cleaning heuristics (Phase 5) and ensuring the test suite passes (Phase 6). Good luck!
