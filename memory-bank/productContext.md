# Product Context for Python Readability

## Why This Project Exists

The Python Readability project exists to provide a high-quality, Python-native implementation of the Readability algorithm. While there are existing Python libraries for content extraction, such as newspaper3k and readability-lxml, they often have limitations or are no longer actively maintained. By porting the well-tested and robust go-readability library to Python, we aim to provide a reliable and up-to-date solution for content extraction in the Python ecosystem.

## Problems It Solves

1. **Content Extraction**: The primary problem this library solves is extracting the main content from HTML pages, removing navigation, ads, and other non-content elements. This is particularly useful for:
   - Web scraping and data mining
   - Creating clean reading experiences
   - Text analysis and natural language processing
   - Archiving web content

2. **Metadata Extraction**: Beyond just the content, the library also extracts important metadata such as:
   - Title
   - Author/byline
   - Publication date
   - Featured image
   - Description/excerpt

3. **Cross-Language Compatibility**: By maintaining compatibility with the Go implementation, the library ensures consistent behavior across different language ecosystems, making it easier to use in polyglot environments.

## How It Should Work

### User Experience

From a user's perspective, the library should be simple to use:

```python
from readability import Readability

# Parse HTML content
parser = Readability()
article, error = parser.parse(html_content, url="https://example.com/article")

if error:
    print(f"Error: {error}")
else:
    # Access extracted content and metadata
    print(f"Title: {article.title}")
    print(f"Byline: {article.byline}")
    print(f"Content: {article.content}")
    print(f"Text Content: {article.text_content}")
    print(f"Excerpt: {article.excerpt}")
    print(f"Site Name: {article.site_name}")
    print(f"Image: {article.image}")
    print(f"Favicon: {article.favicon}")
    print(f"Length: {article.length}")
    print(f"Published Time: {article.published_time}")
```

For CLI usage:

```bash
python -m readability https://example.com/article --output article.html
```

### Internal Workflow

Internally, the library should follow this workflow:

1. **Parse HTML**: Convert the HTML string into a DOM tree using BeautifulSoup.
2. **Preprocess**: Clean up the DOM tree by removing scripts, styles, and other unnecessary elements.
3. **Extract Metadata**: Extract metadata from the DOM tree, such as title, author, and publication date.
4. **Score Content**: Score different parts of the DOM tree to identify the main content.
5. **Extract Content**: Extract the main content based on the scoring.
6. **Postprocess**: Clean up the extracted content, removing any remaining unnecessary elements.
7. **Generate Output**: Generate the final output, including both HTML and plain text versions.

## User Experience Goals

1. **Simplicity**: The library should be easy to use with minimal configuration.
2. **Accuracy**: The library should accurately extract the main content and metadata from a wide variety of websites.
3. **Robustness**: The library should handle edge cases gracefully, such as malformed HTML or unusual page structures.
4. **Performance**: The library should be performant, with minimal memory usage and processing time.
5. **Flexibility**: The library should provide options for customization, such as adjusting the scoring algorithm or specifying which elements to include or exclude.
