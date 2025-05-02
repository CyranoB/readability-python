"""Parser for Python Readability.

This module contains the main Readability class that orchestrates the parsing process
for extracting the main content from HTML pages. It implements a port of the Mozilla
Readability algorithm, which is also used by Firefox's Reader View feature.

The parser works by analyzing the HTML structure, scoring different parts of the page
based on content quality heuristics, and then extracting the highest-scoring section
as the main article content. It also extracts metadata such as title, author, and
publication date.

Example:
    ```python
    from readability import Readability
    
    # Create a parser instance
    parser = Readability()
    
    # Parse HTML content
    with open('article.html', 'r') as f:
        html_content = f.read()
    
    # Extract the article
    article, error = parser.parse(html_content, url='https://example.com/article')
    
    if error:
        print(f"Error: {error}")
    else:
        print(f"Title: {article.title}")
        print(f"Content: {article.content[:100]}...")  # First 100 chars
    ```
"""

import math
import re
import copy
import weakref
import logging
import sys
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Union, Callable, Any
from urllib.parse import urlparse, urljoin

from bs4 import BeautifulSoup, Tag, Comment

from readability.models import Article, ParsingError, ExtractionError
from readability.regexps import RX_DISPLAY_NONE, RX_VISIBILITY_HIDDEN
import readability.regexps as re2go

# Configure logger
logger = logging.getLogger("readability")


class ScoreTracker:
    """Tracks content scores for nodes without modifying them directly.
    
    This class provides a way to associate scores with BeautifulSoup nodes
    without adding attributes to the nodes themselves, which could interfere
    with the DOM structure.
    """
    
    def __init__(self):
        """Initialize an empty score tracker."""
        self._scores = weakref.WeakKeyDictionary()
        
    def set_score(self, node: Tag, score: float) -> None:
        """Set content score for a node.
        
        Args:
            node: The node to set score for
            score: The score value to set
        """
        if node is not None:
            self._scores[node] = float(score)
        
    def get_score(self, node: Tag) -> float:
        """Get content score for a node.
        
        Args:
            node: The node to get score for
            
        Returns:
            The node's score or 0.0 if not set
        """
        return self._scores.get(node, 0.0)
        
    def has_score(self, node: Tag) -> bool:
        """Check if a node has a score assigned.
        
        Args:
            node: The node to check
            
        Returns:
            True if the node has a score, False otherwise
        """
        return node in self._scores
        
    def get_scored_nodes(self) -> List[Tag]:
        """Get all nodes that have scores assigned.
        
        Returns:
            List of nodes with scores
        """
        return list(self._scores.keys())
        
    def clear(self) -> None:
        """Clear all scores."""
        self._scores.clear()


class Readability:
    """Main class for extracting content from HTML pages.

    This class is responsible for parsing HTML content and extracting the main
    article content and metadata. It implements the core algorithm of the
    Readability library and mirrors the Parser struct from the Go implementation
    to maintain compatibility.
    
    The extraction process involves several steps:
    1. Parsing the HTML document
    2. Preprocessing the document (removing scripts, styles, etc.)
    3. Extracting metadata (title, author, publication date, etc.)
    4. Identifying and scoring content nodes
    5. Selecting the best candidate for the main content
    6. Post-processing the content (cleaning up, fixing links, etc.)
    
    The parser uses a scoring algorithm to identify the main content, which
    considers factors like the amount of text, presence of commas, link density,
    and class/ID names.
    """
    
    # Scoring constants
    SCORE_DIV_TAG = 5
    SCORE_PRE_TD_BLOCKQUOTE = 3
    SCORE_ADDRESS_LIST_FORM = -3
    SCORE_HEADING_TH = -5
    SCORE_COMMA_BONUS = 1.0
    SCORE_LENGTH_BONUS_MAX = 3
    SCORE_LENGTH_BONUS_FACTOR = 100
    SCORE_CLASS_WEIGHT_POSITIVE = 25
    SCORE_CLASS_WEIGHT_NEGATIVE = -25
    SCORE_SIBLING_THRESHOLD_FACTOR = 0.2
    SCORE_SIBLING_THRESHOLD_MIN = 10
    MIN_PARAGRAPH_LENGTH = 25

    def __init__(
        self,
        max_elems_to_parse: int = 0,
        n_top_candidates: int = 5,
        char_thresholds: int = 500,
        classes_to_preserve: List[str] = None,
        keep_classes: bool = False,
        tags_to_score: List[str] = None,
        debug: bool = False,
        disable_jsonld: bool = False,
        allowed_video_regex: str = None,
    ):
        """Initialize a new Readability parser with configuration options.

        Args:
            max_elems_to_parse: Maximum number of nodes to parse (0 for no limit).
                Use this to limit processing time for very large documents.
            n_top_candidates: Number of top candidates to consider when selecting
                the main content container. Higher values may improve accuracy but
                increase processing time.
            char_thresholds: Minimum number of characters required for an article
                to be considered valid. If the extracted content is shorter than
                this threshold, the parser will retry with different settings.
            classes_to_preserve: List of CSS class names to preserve in the output.
                By default, most class names are removed to clean up the HTML.
            keep_classes: Whether to keep all CSS classes in the output HTML.
                If True, all classes will be preserved. If False, only classes
                specified in classes_to_preserve will be kept.
            tags_to_score: List of HTML tag names to consider when scoring content.
                These tags are used as starting points for content identification.
            debug: Whether to print debug logs during parsing.
            disable_jsonld: Whether to disable JSON-LD metadata extraction.
                JSON-LD is a structured data format that can provide rich metadata.
            allowed_video_regex: Regular expression pattern for allowed video URLs.
                Videos matching this pattern will be preserved in the output.
                
        Example:
            ```python
            # Create a parser that preserves specific classes
            parser = Readability(
                classes_to_preserve=["highlight", "code"],
                keep_classes=False
            )
            
            # Create a parser with debug output
            parser = Readability(debug=True)
            ```
        """
        self.max_elems_to_parse = max_elems_to_parse
        self.n_top_candidates = n_top_candidates
        self.char_thresholds = char_thresholds
        self.classes_to_preserve = classes_to_preserve or ["page"]
        self.keep_classes = keep_classes
        self.tags_to_score = tags_to_score or [
            "section", "h2", "h3", "h4", "h5", "h6", "p", "td", "pre"
        ]
        self.debug = debug
        self.disable_jsonld = disable_jsonld
        self.allowed_video_regex = allowed_video_regex

        # Internal state
        self.doc = None
        self.document_uri = None
        self.article_title = ""
        self.article_byline = ""
        self.article_dir = ""
        self.article_site_name = ""
        self.article_lang = ""
        self.attempts = []
        self.flags = {
            "strip_unlikelys": True,
            "use_weight_classes": True,
            "clean_conditionally": True,
        }
        
        # Score tracker for managing node scores
        self.score_tracker = ScoreTracker()
        
        # Cache for frequently accessed node properties
        self._cache = {}

    def _get_cache_key(self, node: Tag, operation: str) -> str:
        """Generate a cache key for node operations.
        
        Args:
            node: The node to generate a key for
            operation: The operation being performed
            
        Returns:
            A unique cache key for the node and operation
        """
        # Use the node's id as a key
        node_id = id(node)
        return f"{node_id}:{operation}"
    
    def parse(
        self, html_content: Union[str, bytes], url: Optional[str] = None,
        encoding: Optional[str] = None
    ) -> Tuple[Optional[Article], Optional[Exception]]:
        """Parse HTML content and extract the main article.

        This is the main entry point for the Readability parser. It orchestrates
        the parsing process and returns either an Article object or an error.
        
        The method follows the Go implementation's error handling pattern by
        returning a tuple of (result, error) where one is always None. This
        makes error handling explicit and avoids raising exceptions for expected
        failure cases.

        Args:
            html_content: HTML content as string or bytes. If bytes are provided,
                the encoding will be automatically detected by BeautifulSoup/lxml.
            url: Optional URL for the HTML content. This is used for resolving
                relative links in the document and for extracting the base URL
                for metadata.
            encoding: Optional character encoding to use when parsing bytes.
                If None, encoding will be auto-detected.
                Ignored when html_content is a string.

        Returns:
            A tuple of (article, error) where one is None. If successful, the
            first element will be an Article object containing the extracted
            content and metadata. If unsuccessful, the second element will be
            an Exception describing the error.
            
        Example:
            ```python
            # Parse HTML from a string
            article, error = parser.parse("<html><body><p>Content</p></body></html>")
            
            # Parse HTML from a file with a URL for resolving relative links
            with open("article.html", "r") as f:
                html_content = f.read()
            article, error = parser.parse(html_content, url="https://example.com/article")
            
            # Parse HTML with explicit encoding
            with open("article.html", "rb") as f:
                html_content = f.read()
            article, error = parser.parse(html_content, encoding="utf-8")
            
            # Handle errors explicitly
            if error:
                print(f"Failed to parse: {error}")
            else:
                print(f"Extracted article: {article.title}")
            ```
            
        Encoding Handling:

        When processing HTML content, character encoding is crucial for correct text extraction.
        The parser handles encoding in the following ways:

        1. If html_content is a string, it's assumed to be properly decoded already.
        2. If html_content is bytes:
           - If encoding is specified, that encoding is used
           - Otherwise, the encoding is auto-detected by BeautifulSoup/lxml

        If you encounter garbled text with strange characters like 'Ã¢', 'Ã©', etc.,
        try specifying the correct encoding explicitly.

        Common encodings:
        - 'utf-8' (default in modern web)
        - 'iso-8859-1' (Latin-1)
        - 'windows-1252' (Common in Windows systems)
        - 'euc-jp', 'shift-jis' (Japanese content)
        - 'gb2312', 'gbk' (Chinese content)
        - 'koi8-r' (Russian content)
        """
        # Clear cache at the start of parsing
        self._cache = {}
        try:
            # Handle encoding based on input type
            if isinstance(html_content, bytes):
                # If bytes provided with explicit encoding
                if encoding:
                    # Use the specified encoding
                    self.doc = BeautifulSoup(html_content, "lxml", from_encoding=encoding)
                else:
                    # Let BeautifulSoup auto-detect encoding
                    self.doc = BeautifulSoup(html_content, "lxml")
                    
                # Check encoding detection result for debugging
                if self.debug:
                    detected = self.doc.original_encoding
                    logger.debug(f"Detected encoding: {detected}")
            else:
                # For string input, assume it's already properly decoded
                self.doc = BeautifulSoup(html_content, "lxml")
            
            # Validate encoding
            encoding_error = self._validate_encoding(self.doc)
            if encoding_error:
                if self.debug:
                    logger.warning(f"Encoding warning: {encoding_error}")
                
                # If explicit encoding was provided but still got errors, return an error
                if encoding and isinstance(html_content, bytes):
                    return None, ParsingError(f"Encoding error: {encoding_error}. " 
                                            f"Specified encoding '{encoding}' may be incorrect.")
            
            # Set document URI if provided
            if url:
                self.document_uri = urlparse(url)
            
            # Reset parser data
            self.article_title = ""
            self.article_byline = ""
            self.article_dir = ""
            self.article_site_name = ""
            self.article_lang = ""
            self.attempts = []
            self.flags = {
                "strip_unlikelys": True,
                "use_weight_classes": True,
                "clean_conditionally": True,
            }
            
            # Check if document is too large
            if self.max_elems_to_parse > 0:
                num_elements = len(self.doc.find_all())
                if num_elements > self.max_elems_to_parse:
                    return None, ParsingError(f"Document too large: {num_elements} elements")
            
            # Unwrap images from noscript tags
            self._unwrap_noscript_images()
            
            # Extract JSON-LD metadata before removing scripts
            json_ld = {}
            if not self.disable_jsonld:
                json_ld = self._get_json_ld()
            
            # Remove script tags
            self._remove_scripts()
            
            # Prepare document for parsing
            self._prep_document()
            
            # Get article title
            self.article_title = self._get_article_title()
            
            # Get article metadata
            metadata = self._get_metadata(json_ld)
            
            # Grab article content
            article_content = self._grab_article()
            if article_content is None:
                return None, ParsingError("Could not extract article content")
            
            # Post-process content
            self._postprocess_content(article_content)
            
            # Extract excerpt from first paragraph if not found in metadata
            if metadata.get("excerpt", "") == "" and article_content is not None:
                paragraphs = article_content.find_all("p")
                if paragraphs:
                    metadata["excerpt"] = paragraphs[0].get_text().strip()
            
            # Get readable node (first element child of article content)
            readable_node = None
            if article_content is not None and article_content.contents:
                for child in article_content.contents:
                    if child.name is not None:  # Skip text nodes
                        readable_node = child
                        break
            
            # Get final HTML and text content
            final_html_content = str(article_content) if article_content else ""
            final_text_content = self._get_inner_text(article_content) if article_content else ""
            
            # Get final byline
            final_byline = metadata.get("byline", "") or self.article_byline
            
            # Clean up excerpt (remove newlines)
            excerpt = metadata.get("excerpt", "").strip()
            excerpt = " ".join(excerpt.split())
            
            # Parse dates
            published_time = self._parse_date(metadata.get("publishedTime"))
            modified_time = self._parse_date(metadata.get("modifiedTime"))
            
            # Create Article object
            article = Article(
                url=url,
                title=metadata.get("title", self.article_title),
                byline=final_byline,
                node=readable_node,
                content=final_html_content,
                text_content=final_text_content,
                length=len(final_text_content),
                excerpt=excerpt,
                site_name=metadata.get("siteName"),
                image=metadata.get("image"),
                favicon=metadata.get("favicon"),
                language=self.article_lang,
                published_time=published_time,
                modified_time=modified_time,
            )
            
            return article, None
        
        except Exception as e:
            return None, e

    def _text_similarity(self, text_a: str, text_b: str) -> float:
        """Compare second text to first one.
        
        1 = same text, 0 = completely different text.
        The way it works: it splits both texts into words and then finds words
        that are unique in second text. The result is given by the lower length
        of unique parts.
        
        Args:
            text_a: First text to compare
            text_b: Second text to compare
            
        Returns:
            Similarity score between 0 and 1
        """
        import re
        from readability.regexps import RX_TOKENIZE
        
        # Tokenize texts
        tokens_a = RX_TOKENIZE.split(text_a.lower())
        tokens_a = [token for token in tokens_a if token]
        
        tokens_b = RX_TOKENIZE.split(text_b.lower())
        tokens_b = [token for token in tokens_b if token]
        
        # Create a set of tokens from text A for faster lookup
        tokens_a_set = set(tokens_a)
        
        # Find unique tokens in text B (not in text A)
        unique_tokens_b = [token for token in tokens_b if token not in tokens_a_set]
        
        # Calculate similarity
        merged_b = " ".join(tokens_b)
        merged_unique_b = " ".join(unique_tokens_b)
        
        if not merged_b:
            return 0
        
        distance_b = len(merged_unique_b) / len(merged_b)
        return 1 - distance_b

    def _prep_document(self) -> None:
        """Prepare document for parsing.
        
        This includes removing scripts, styles, and handling terrible markup.
        """
        # Remove all comments
        self._remove_comments()
        
        # Remove all style tags in head
        for style in self.doc.find_all("style"):
            style.decompose()
        
        # Find body and replace <br> tags
        body = self.doc.find("body")
        if body:
            self._replace_brs(body)
        
        # Replace font tags with span
        for font in self.doc.find_all("font"):
            font.name = "span"

    def _remove_comments(self) -> None:
        """Remove all comments from the document."""
        comments = self.doc.find_all(string=lambda text: isinstance(text, Comment))
        for comment in comments:
            comment.extract()

    def _replace_brs(self, elem: Tag) -> None:
        """Replace 2 or more successive <br> with a single <p>.
        
        Whitespace between <br> elements are ignored. For example:
        
            <div>foo<br>bar<br> <br><br>abc</div>
        
        will become:
        
            <div>foo<br>bar<p>abc</p></div>
        """
        # Find all <br> elements
        brs = elem.find_all("br")
        for br in brs:
            # Get next node, skipping whitespace
            next_node = br.next_sibling
            while next_node and (next_node.name is None and not next_node.strip()):
                next_node = next_node.next_sibling
            
            # If we don't find a <br> chain, continue
            if not next_node or next_node.name != "br":
                continue
            
            # We have at least 2 <br> elements in a row, so this is a <br> chain
            # Remove all but the first <br>
            replaced = False
            while next_node and next_node.name == "br":
                replaced = True
                br_sibling = next_node.next_sibling
                next_node.decompose()
                next_node = br_sibling
                
                # Skip whitespace
                while next_node and (next_node.name is None and not next_node.strip()):
                    next_node = next_node.next_sibling
            
            # If we removed a <br> chain, replace the remaining <br> with a <p>
            if replaced:
                p = self.doc.new_tag("p")
                br.replace_with(p)
                
                # Add all sibling nodes as children of the <p> until we hit another <br> chain
                next_node = p.next_sibling
                while next_node:
                    # If we've hit another <br><br>, we're done adding children to this <p>
                    if next_node.name == "br":
                        next_elem = next_node.next_sibling
                        while next_elem and (next_elem.name is None and not next_elem.strip()):
                            next_elem = next_elem.next_sibling
                        if next_elem and next_elem.name == "br":
                            break
                    
                    # If we hit a block element, we're done
                    if next_node.name and next_node.name in ["div", "p", "blockquote", "pre", "table"]:
                        break
                    
                    # Otherwise, make this node a child of the new <p>
                    sibling = next_node.next_sibling
                    p.append(next_node)
                    next_node = sibling
                
                # Remove trailing whitespace from the <p>
                if p.contents:
                    last_child = p.contents[-1]
                    if last_child.name is None and not last_child.strip():
                        last_child.extract()
                
                # If the <p> is inside another <p>, change the parent to a <div>
                if p.parent and p.parent.name == "p":
                    p.parent.name = "div"

    def _get_article_title(self) -> str:
        """Extract the article title from the document."""
        from readability.regexps import RX_TITLE_SEPARATOR, RX_TITLE_HIERARCHY_SEP, RX_TITLE_REMOVE_FINAL_PART
        from readability.regexps import RX_TITLE_REMOVE_1ST_PART, RX_TITLE_ANY_SEPARATOR
        from readability.utils import word_count, char_count, normalize_spaces
        
        doc = self.doc
        cur_title = ""
        orig_title = ""
        title_had_hierarchical_separators = False
        
        # If they had an element with tag "title" in their HTML
        title_tag = doc.find("title")
        if title_tag:
            orig_title = self._get_inner_text(title_tag, True)
            cur_title = orig_title
        
        # If there's a separator in the title, first remove the final part
        if RX_TITLE_SEPARATOR.search(cur_title):
            title_had_hierarchical_separators = bool(RX_TITLE_HIERARCHY_SEP.search(cur_title))
            match = RX_TITLE_REMOVE_FINAL_PART.search(orig_title)
            if match:
                cur_title = match.group(1)
                
                # If the resulting title is too short (3 words or fewer), remove
                # the first part instead
                if word_count(cur_title) < 3:
                    match = RX_TITLE_REMOVE_1ST_PART.search(orig_title)
                    if match:
                        cur_title = match.group(1)
        
        # If we now have 4 words or fewer as our title, and either no
        # 'hierarchical' separators (\, /, > or ») were found in the original
        # title or we decreased the number of words by more than 1 word, use
        # the original title.
        cur_title = cur_title.strip()
        cur_title = normalize_spaces(cur_title)
        
        if word_count(cur_title) <= 4:
            tmp_orig_title = RX_TITLE_ANY_SEPARATOR.sub("", orig_title)
            if not title_had_hierarchical_separators or word_count(cur_title) != word_count(tmp_orig_title) - 1:
                cur_title = orig_title
        
        return cur_title

    def _unwrap_noscript_images(self) -> None:
        """Find all <noscript> that are located after <img> nodes,
        and which contain only one <img> element. Replace the first image
        with the image from inside the <noscript> tag, and remove the
        <noscript> tag. This improves the quality of the images we use on
        some sites (e.g. Medium).
        """
        from readability.regexps import RX_IMG_EXTENSIONS
        
        # Find img without source or attributes that might contain image, and
        # remove it. This is done to prevent a placeholder img being replaced by
        # img from noscript in next step.
        imgs = self.doc.find_all("img")
        for img in imgs:
            has_valid_attrs = False
            for attr_name, attr_value in img.attrs.items():
                # Handle AttributeValueList objects
                if isinstance(attr_value, list):
                    attr_value = " ".join(attr_value)
                
                if attr_name in ["src", "data-src", "srcset", "data-srcset"]:
                    has_valid_attrs = True
                    break
                
                if attr_value and RX_IMG_EXTENSIONS.search(attr_value):
                    has_valid_attrs = True
                    break
            
            if not has_valid_attrs and img.parent:
                img.decompose()
        
        # Next find noscript and try to extract its image
        noscripts = self.doc.find_all("noscript")
        for noscript in noscripts:
            # Parse content of noscript and make sure it only contains image
            noscript_content = noscript.get_text()
            try:
                tmp_doc = BeautifulSoup(noscript_content, "lxml")
                tmp_body = tmp_doc.body
                
                if not tmp_body or not self._is_single_image(tmp_body):
                    continue
                
                # If noscript has previous sibling and it only contains image,
                # replace it with noscript content. However, we also keep old
                # attributes that might contain image.
                prev_element = noscript.find_previous_sibling()
                if prev_element and self._is_single_image(prev_element):
                    prev_img = prev_element
                    if prev_img.name != "img":
                        prev_img = prev_img.find("img")
                    
                    new_img = tmp_body.find("img")
                    if not new_img:
                        continue
                    
                    # Copy attributes from old image to new image
                    for attr_name, attr_value in prev_img.attrs.items():
                        if not attr_value:
                            continue
                        
                        if attr_name in ["src", "srcset"] or RX_IMG_EXTENSIONS.search(attr_value):
                            if new_img.get(attr_name) == attr_value:
                                continue
                            
                            attr_name_to_use = attr_name
                            if attr_name in new_img.attrs:
                                attr_name_to_use = f"data-old-{attr_name}"
                            
                            new_img[attr_name_to_use] = attr_value
                    
                    # Replace old image with new image
                    prev_element.replace_with(new_img)
            except Exception:
                # If parsing fails, just continue
                continue

    def _is_single_image(self, node: Tag) -> bool:
        """Check if node is image, or if node contains exactly
        only one image whether as a direct child or as its descendants.
        """
        if node.name == "img":
            return True
        
        # Check if node has exactly one child and no text content
        children = [child for child in node.children if child.name is not None]
        if len(children) != 1 or node.get_text().strip():
            return False
        
        # Check if the single child is an image or contains an image
        return self._is_single_image(children[0])

    def _remove_scripts(self) -> None:
        """Remove script tags from the document."""
        for script in self.doc.find_all(["script", "noscript"]):
            script.decompose()

    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse a date string into a datetime object.
        
        Args:
            date_str: The date string to parse
            
        Returns:
            A datetime object or None if parsing fails
        """
        if not date_str:
            return None
        
        try:
            from dateutil.parser import parse
            return parse(date_str)
        except Exception:
            if self.debug:
                logger.debug(f"Failed to parse date: {date_str}")
            return None

    def _get_json_ld(self) -> Dict[str, str]:
        """Extract metadata from JSON-LD objects.
        
        For now, only Schema.org objects of type Article or its subtypes are supported.
        
        Returns:
            A dictionary of metadata extracted from JSON-LD
        """
        import json
        import re
        from readability.regexps import RX_CDATA, RX_SCHEMA_ORG, RX_JSON_LD_ARTICLE_TYPES
        
        metadata = {}
        
        # Find all JSON-LD scripts
        scripts = self.doc.select('script[type="application/ld+json"]')
        for script in scripts:
            if metadata:  # Already found metadata
                break
            
            # Strip CDATA markers if present
            content = script.string or ""
            content = RX_CDATA.sub("", content)
            
            try:
                # Parse JSON
                try:
                    parsed = json.loads(content)
                except json.JSONDecodeError as e:
                    if self.debug:
                        logger.debug(f"Failed to parse JSON-LD: {e}")
                    continue
                
                # Check context
                context = parsed.get("@context", "")
                if not isinstance(context, str) or not RX_SCHEMA_ORG.search(context):
                    continue
                
                # If parsed doesn't have any @type, find it in its graph list
                if "@type" not in parsed:
                    graph_list = parsed.get("@graph", [])
                    if not isinstance(graph_list, list):
                        continue
                    
                    for graph in graph_list:
                        if not isinstance(graph, dict):
                            continue
                        
                        graph_type = graph.get("@type", "")
                        if isinstance(graph_type, str) and RX_JSON_LD_ARTICLE_TYPES.search(graph_type):
                            parsed = graph
                            break
                
                # Once again, make sure parsed has valid @type
                parsed_type = parsed.get("@type", "")
                if not isinstance(parsed_type, str) or not RX_JSON_LD_ARTICLE_TYPES.search(parsed_type):
                    continue
                
                # Extract metadata
                metadata = {}
                
                # Title
                name = parsed.get("name", "")
                headline = parsed.get("headline", "")
                
                if name and headline and name != headline:
                    # We have both name and headline element in the JSON-LD. They should both be the same
                    # but some websites put their own name into "name" and the article
                    # title to "headline" which confuses Readability. So we try to check if either "name"
                    # or "headline" closely matches the html title, and if so, use that one. If not, then
                    # we use "name" by default.
                    title = self._get_article_title()
                    name_matches = self._text_similarity(name, title) > 0.75
                    headline_matches = self._text_similarity(headline, title) > 0.75
                    
                    if headline_matches and not name_matches:
                        metadata["title"] = headline
                    else:
                        metadata["title"] = name
                elif name:
                    metadata["title"] = name.strip()
                elif headline:
                    metadata["title"] = headline.strip()
                
                # Author
                author = parsed.get("author", {})
                if isinstance(author, dict):
                    author_name = author.get("name", "")
                    if author_name:
                        metadata["byline"] = author_name.strip()
                elif isinstance(author, list):
                    author_names = []
                    for auth in author:
                        if isinstance(auth, dict):
                            author_name = auth.get("name", "")
                            if author_name:
                                author_names.append(author_name.strip())
                    
                    if author_names:
                        metadata["byline"] = ", ".join(author_names)
                
                # Description
                description = parsed.get("description", "")
                if description:
                    metadata["excerpt"] = description.strip()
                
                # Publisher
                publisher = parsed.get("publisher", {})
                if isinstance(publisher, dict):
                    publisher_name = publisher.get("name", "")
                    if publisher_name:
                        metadata["siteName"] = publisher_name.strip()
                
                # DatePublished
                date_published = parsed.get("datePublished", "")
                if date_published:
                    metadata["datePublished"] = date_published
                
                # DateModified
                date_modified = parsed.get("dateModified", "")
                if date_modified:
                    metadata["dateModified"] = date_modified
                
            except Exception:
                # If parsing fails, just continue
                continue
        
        return metadata

    def _get_metadata(self, json_ld: Dict[str, str] = None) -> Dict[str, str]:
        """Extract metadata from the document.
        
        This includes title, byline, excerpt, site name, etc.
        
        Args:
            json_ld: Optional metadata from JSON-LD
            
        Returns:
            A dictionary of metadata
        """
        import html
        from readability.regexps import RX_PROPERTY_PATTERN, RX_NAME_PATTERN
        
        json_ld = json_ld or {}
        values = {}
        
        # Find meta elements
        meta_elements = self.doc.find_all("meta")
        
        # Extract metadata from meta tags
        for element in meta_elements:
            # Handle potential AttributeValueList objects
            element_name = self._normalize_attr_value(element.get("name", ""))
            element_property = self._normalize_attr_value(element.get("property", ""))
            content = self._normalize_attr_value(element.get("content", ""))
            
            if not content:
                continue
            
            matches = []
            name = ""
            
            if element_property:
                matches = RX_PROPERTY_PATTERN.findall(element_property)
                for match in matches:
                    # Convert to lowercase, and remove any whitespace
                    name = match[0].lower() + ":" + match[1].lower()
                    name = "".join(name.split())
                    values[name] = content.strip()
            
            if not matches and element_name and RX_NAME_PATTERN.search(element_name):
                # Convert to lowercase, remove any whitespace, and convert
                # dots to colons
                name = element_name.lower()
                name = "".join(name.split())
                name = name.replace(".", ":")
                values[name] = content.strip()
        
        # Get title
        metadata_title = (
            json_ld.get("title") or
            values.get("dc:title") or
            values.get("dcterm:title") or
            values.get("og:title") or
            values.get("weibo:article:title") or
            values.get("weibo:webpage:title") or
            values.get("title") or
            values.get("twitter:title") or
            self._get_article_title()
        )
        
        # Get author
        metadata_byline = (
            json_ld.get("byline") or
            values.get("dc:creator") or
            values.get("dcterm:creator") or
            values.get("author")
        )
        
        # Get description
        metadata_excerpt = (
            json_ld.get("excerpt") or
            values.get("dc:description") or
            values.get("dcterm:description") or
            values.get("og:description") or
            values.get("weibo:article:description") or
            values.get("weibo:webpage:description") or
            values.get("description") or
            values.get("twitter:description")
        )
        
        # Get site name
        metadata_site_name = json_ld.get("siteName") or values.get("og:site_name")
        
        # Get image thumbnail
        metadata_image = (
            values.get("og:image") or
            values.get("image") or
            values.get("twitter:image")
        )
        
        # Get favicon
        metadata_favicon = self._get_article_favicon()
        
        # Get published date
        metadata_published_time = (
            json_ld.get("datePublished") or
            values.get("article:published_time") or
            values.get("dcterms.available") or
            values.get("dcterms.created") or
            values.get("dcterms.issued") or
            values.get("weibo:article:create_at")
        )
        
        # Get modified date
        metadata_modified_time = (
            json_ld.get("dateModified") or
            values.get("article:modified_time") or
            values.get("dcterms.modified")
        )
        
        # Unescape HTML entities
        metadata_title = html.unescape(metadata_title or "")
        metadata_byline = html.unescape(metadata_byline or "")
        metadata_excerpt = html.unescape(metadata_excerpt or "")
        metadata_site_name = html.unescape(metadata_site_name or "")
        metadata_published_time = html.unescape(metadata_published_time or "")
        metadata_modified_time = html.unescape(metadata_modified_time or "")
        
        return {
            "title": metadata_title,
            "byline": metadata_byline,
            "excerpt": metadata_excerpt,
            "siteName": metadata_site_name,
            "image": metadata_image,
            "favicon": metadata_favicon,
            "publishedTime": metadata_published_time,
            "modifiedTime": metadata_modified_time,
        }

    def _score_paragraphs(self) -> List[Tag]:
        """Score paragraphs and their parent nodes.
        
        This method finds all paragraphs and other content elements,
        calculates their content scores, and propagates those scores
        to parent nodes. This helps identify the main content container.
        
        Returns:
            List of candidate nodes with scores
        """
        candidates = []
        
        # Find all potential paragraph elements
        paragraphs = []
        for tag_name in self.tags_to_score:
            paragraphs.extend(self.doc.find_all(tag_name))
        
        for paragraph in paragraphs:
            parent = paragraph.parent
            
            # Skip elements that aren't visible or have no parent
            if not parent or not self._is_probably_visible(paragraph):
                continue
                
            # If this paragraph is less than 25 characters, don't count it
            inner_text = self._get_inner_text(paragraph)
            if len(inner_text) < 25:
                continue
                
            # Get ancestors up to 3 levels back
            ancestors = self._get_node_ancestors(paragraph, 3)
            
            # Initialize ancestors that don't have scores yet
            for ancestor in ancestors:
                if not self.score_tracker.has_score(ancestor):
                    self._initialize_node(ancestor)
                    candidates.append(ancestor)
            
            # Calculate paragraph's content score
            paragraph_score = self._calculate_content_score(paragraph)
            
            # Add to ancestor scores with diminishing effect by level
            for i, ancestor in enumerate(ancestors):
                score_divider = 1 if i == 0 else 2 if i == 1 else i * 3
                current_score = self.score_tracker.get_score(ancestor)
                self.score_tracker.set_score(ancestor, current_score + (paragraph_score / score_divider))
        
        return candidates

    def _select_best_candidate(self, candidates: List[Tag]) -> Optional[Tag]:
        """Select the best candidate from scored nodes.
        
        Args:
            candidates: List of candidate nodes with scores
            
        Returns:
            The best candidate node or None if no candidates
        """
        if not candidates:
            return None
        
        # Sort candidates by score (descending)
        sorted_candidates = sorted(
            candidates, 
            key=lambda x: self.score_tracker.get_score(x),
            reverse=True
        )
        
        # Take the highest scored candidate
        if not sorted_candidates:
            return None
            
        top_candidate = sorted_candidates[0]
        
        # If we have only one candidate, use it
        if len(sorted_candidates) == 1:
            return top_candidate
        
        # Get the top candidate score
        top_score = self.score_tracker.get_score(top_candidate)
        
        # Look for a better candidate in the hierarchy
        # Check parents for better scores
        parent = top_candidate.parent
        score_threshold = top_score / 3.0
        
        # Loop up through parent hierarchy
        while parent and parent.name != "body":
            # Skip parents that don't have a score
            if not self.score_tracker.has_score(parent):
                parent = parent.parent
                continue
                
            parent_score = self.score_tracker.get_score(parent)
            if parent_score < score_threshold:
                break
                
            if parent_score > top_score:
                # Found a better parent!
                top_candidate = parent
                top_score = parent_score
                
            parent = parent.parent
        
        # Check the "only child" scenario - use parent if it has only one child
        parent = top_candidate.parent
        while parent and parent.name != "body":
            children = parent.find_all(True, recursive=False)  # direct children
            if len(children) != 1:
                break
            top_candidate = parent
            parent = parent.parent
        
        return top_candidate

    def _construct_article_content(self, top_candidate: Tag) -> Tag:
        """Construct article content from top candidate and related nodes.
        
        Args:
            top_candidate: The best candidate node
            
        Returns:
            Article content container with all relevant content
        """
        # Create article container with proper ID and class
        article_content = BeautifulSoup('<div id="readability-page-1" class="page"></div>', "lxml").div
        
        if not top_candidate:
            # If no top candidate, create a container for the entire body
            body = self.doc.find("body")
            if body:
                for child in list(body.children):  # Copy to avoid modification during iteration
                    # Skip non-visible elements and H1 elements (title)
                    if not self._is_probably_visible(child) or child.name == "h1":
                        continue
                    article_content.append(copy.copy(child))
            return article_content
        
        # Calculate threshold for sibling content inclusion
        top_score = self.score_tracker.get_score(top_candidate)
        threshold = max(10, top_score * 0.2)
        
        # Get parent of top candidate to find siblings
        parent = top_candidate.parent
        siblings = list(parent.children) if parent else []
        
        # Examine each sibling for potential inclusion
        for sibling in siblings:
            append = False
            
            # Skip elements that aren't visible or are H1 elements (title)
            if not self._is_probably_visible(sibling) or sibling.name == "h1":
                continue
                
            if sibling is top_candidate:
                # Always include the top candidate
                append = True
            elif self.score_tracker.has_score(sibling) and self.score_tracker.get_score(sibling) >= threshold:
                # Include siblings that score above threshold
                append = True
            elif sibling.name == "p":
                # Special handling for paragraphs
                link_density = self._get_link_density(sibling)
                text = self._get_inner_text(sibling)
                text_length = len(text)
                
                if text_length > 80 and link_density < 0.25:
                    # Long paragraphs with low link density
                    append = True
                elif text_length < 80 and link_density == 0 and re.search(r'\.( |$)', text):
                    # Short paragraphs ending with period and no links
                    append = True
            
            if append:
                # Create a deep copy of the sibling to avoid modifying original
                sibling_copy = copy.deepcopy(sibling)
                
                # Add proper indentation
                article_content.append("        ")
                
                if sibling.name == "div" or sibling.name == "article" or sibling.name == "p":
                    # These elements can be appended directly
                    article_content.append(sibling_copy)
                else:
                    # Other elements should be wrapped in a div
                    new_div = BeautifulSoup("<div></div>", "lxml").div
                    new_div.append(sibling_copy)
                    article_content.append(new_div)
                
                # Add newline after each element
                article_content.append("\n")
        
        return article_content

    def _grab_article(self) -> Optional[Tag]:
        """Extract the main article content from the document.
        
        This is the heart of the readability algorithm.
        
        Returns:
            Article content or None if extraction fails
        """
        # Track attempts for retry with different flags
        self.attempts = []
        
        # Define flag configurations to try in order
        flag_configurations = [
            {"strip_unlikelys": True, "use_weight_classes": True, "clean_conditionally": True},
            {"strip_unlikelys": False, "use_weight_classes": True, "clean_conditionally": True},
            {"strip_unlikelys": False, "use_weight_classes": False, "clean_conditionally": True},
            {"strip_unlikelys": False, "use_weight_classes": False, "clean_conditionally": False}
        ]
        
        # Try each flag configuration until we get good content or exhaust options
        for flags in flag_configurations:
            # Update flags for this attempt
            self.flags = flags
            
            # Phase 1: Clean and prepare the document
            self._remove_unlikely_candidates()
            self._transform_misused_divs_into_paragraphs()
            
            # Phase 2: Score paragraphs
            candidates = self._score_paragraphs()
            
            # Phase 3: Select the best candidate
            top_candidate = self._select_best_candidate(candidates)
            
            # Phase 4: Construct the article content
            article_content = self._construct_article_content(top_candidate)
            
            # Track this attempt
            if article_content:
                inner_text = self._get_inner_text(article_content)
                content_length = len(inner_text)
                self.attempts.append({
                    "article_content": article_content,
                    "length": content_length,
                    "flags": flags.copy()
                })
                
                # If content is long enough, we're done
                if content_length >= self.char_thresholds:
                    return article_content
        
        # If we get here, we've tried all configurations and nothing worked well
        # Return the best attempt we have
        best_attempt = None
        max_length = 0
        
        for attempt in self.attempts:
            if attempt["length"] > max_length:
                max_length = attempt["length"]
                best_attempt = attempt["article_content"]
                
        return best_attempt

    def _remove_unlikely_candidates(self) -> None:
        """Remove nodes that are unlikely to be content.
        
        This includes navigation, ads, etc. based on class and ID names.
        """
        if not self.flags["strip_unlikelys"]:
            return
        
        for elem in self.doc.find_all(True):
            # Skip elements that are definitely content
            if elem.name in ["html", "body", "article", "a"]:
                continue
                
            # Check if element has ancestor table or code
            if self._has_ancestor_tag(elem, "table", 3, None) or \
               self._has_ancestor_tag(elem, "code", 3, None):
                continue
                
            # Check class and ID for unlikely patterns
            class_value = self._normalize_attr_value(elem.get('class', []))
            id_value = self._normalize_attr_value(elem.get('id', ''))
            match_string = f"{class_value} {id_value}"
            
            # Use imported re2go functions from regexps.py
            if re2go.is_unlikely_candidate(match_string) and \
               not re2go.maybe_its_a_candidate(match_string):
                # Remove the element
                elem.extract()

    def _transform_misused_divs_into_paragraphs(self) -> None:
        """Transform divs that are misused as paragraphs into p tags.
        
        Many sites use divs instead of p tags for paragraphs, which can
        confuse the scoring algorithm. This method converts such divs to p tags.
        """
        # Define block elements that shouldn't be transformed
        block_elems = ["div", "p", "blockquote", "pre", "table", "ul", "ol", "h1", "h2", "h3", "h4", "h5", "h6"]
        
        for elem in self.doc.find_all("div"):
            # Skip divs that have block elements as children
            has_block = False
            for child in elem.find_all(True, recursive=False):
                if child.name in block_elems:
                    has_block = True
                    break
            
            if not has_block:
                # This div doesn't contain other block elements, convert it
                elem.name = "p"
                
                # Optional: clean up any unnecessary attributes
                for attr in list(elem.attrs.keys()):
                    if attr not in ["id", "class"]:
                        del elem[attr]

    def _clean_classes(self, node: Tag) -> None:
        """Remove all class attributes from a node and its descendants.
        
        Preserves classes specified in classes_to_preserve.
        
        Args:
            node: The node to clean classes from
        """
        if not node:
            return
        
        # Clean classes from the node itself
        if node.has_attr("class"):
            # Check if any classes should be preserved
            classes_to_keep = []
            for class_name in node.get("class", []):
                if class_name in self.classes_to_preserve:
                    classes_to_keep.append(class_name)
            
            if classes_to_keep:
                node["class"] = classes_to_keep
            else:
                del node["class"]
        
        # Clean classes from all descendants
        for child in node.find_all(True, recursive=False):
            self._clean_classes(child)

    def _clean_conditionally(self, node: Tag, tag_name: str) -> None:
        """Clean a node of all tags of type 'tag_name' if they look fishy.
        
        "Fishy" is based on content length, link density, etc.
        
        Args:
            node: The node to clean
            tag_name: The tag name to clean (e.g., "div", "table", "form")
        """
        if not self.flags["clean_conditionally"]:
            return
        
        # Find all elements with the specified tag
        elems_to_check = node.find_all(tag_name)
        
        for elem in elems_to_check:
            weight = self._get_class_weight(elem)
            content_score = self.score_tracker.get_score(elem) + weight
            
            # Skip data tables
            if tag_name == "table" and self._is_data_table(elem):
                continue
                
            # Check ancestors - don't remove elements inside good content
            if self._has_ancestor_tag(elem, "table", -1, self._is_data_table):
                continue
                
            if content_score >= 0:
                continue
                
            # Check specific characteristics that indicate non-content
            
            # 1. Check for few commas
            if self._get_inner_text(elem).count(",") < 10:
                # Count various elements
                p_count = len(elem.find_all("p"))
                img_count = len(elem.find_all("img"))
                li_count = len(elem.find_all("li")) - 100  # Penalize long lists
                input_count = len(elem.find_all("input"))
                
                # Calculate content density
                content_length = len(self._get_inner_text(elem))
                link_density = self._get_link_density(elem)
                
                # Various heuristic checks
                if img_count > 1 and p_count / img_count < 0.5:
                    elem.extract()
                    continue
                    
                if li_count > p_count and tag_name != "ul" and tag_name != "ol":
                    elem.extract()
                    continue
                    
                if input_count > p_count / 3:
                    elem.extract()
                    continue
                    
                if content_length < 25 and (img_count == 0 or img_count > 2):
                    elem.extract()
                    continue
                    
                if weight < 25 and link_density > 0.2:
                    elem.extract()
                    continue
                    
                if weight >= 25 and link_density > 0.5:
                    elem.extract()
                    continue

    def _is_data_table(self, table: Tag) -> bool:
        """Check if a table is a data table rather than a layout table.
        
        Data tables are preserved, while layout tables might be removed.
        
        Args:
            table: The table to check
            
        Returns:
            True if the table is a data table, False otherwise
        """
        # Check for common data table attributes
        if table.has_attr("role") and table["role"] == "grid":
            return True
        
        # Check for caption
        if table.find("caption"):
            return True
        
        # Check for table header cells
        if table.find("th"):
            return True
        
        # Check for colgroup or col elements
        if table.find("colgroup") or table.find("col"):
            return True
        
        # Check for structured rows and cells
        rows = table.find_all("tr")
        if not rows:
            return False
        
        # Check if all rows have the same number of cells
        first_row_cells = len(rows[0].find_all(["td", "th"]))
        if first_row_cells == 0:
            return False
        
        # Check if at least 80% of rows have the same number of cells
        same_cells_count = 0
        for row in rows:
            if len(row.find_all(["td", "th"])) == first_row_cells:
                same_cells_count += 1
        
        if same_cells_count / len(rows) >= 0.8:
            return True
        
        return False

    def _clean_headers(self, article_content: Tag) -> None:
        """Clean out spurious headers from an article.
        
        Checks things like classnames and link density.
        
        Args:
            article_content: The article content to clean headers from
        """
        # Find all h1, h2, h3, h4, h5, h6 elements
        headers = article_content.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
        
        for header in headers:
            # Check if header should be removed
            weight = self._get_class_weight(header)
            
            # If the header has a negative weight or high link density, remove it
            if weight < 0 or self._get_link_density(header) > 0.33:
                header.extract()

    def _prepare_article(self, article_content: Tag) -> None:
        """Prepare the article for display.
        
        Clean out any inline styles, remove empty nodes, etc.
        
        Args:
            article_content: The article content to prepare
        """
        if not article_content:
            return
        
        # Remove empty nodes
        self._remove_empty_nodes(article_content)
        
        # Ensure proper paragraph structure
        self._ensure_paragraph_structure(article_content)

    def _remove_empty_nodes(self, node: Tag) -> None:
        """Remove nodes with no content.
        
        Args:
            node: The node to check and clean
        """
        for child in list(node.children):
            if child.name is not None:  # Only process element nodes
                # Check if the node is empty (no text and no non-empty children)
                if not child.get_text().strip() and not child.find_all(True):
                    child.extract()
                else:
                    # Recursively check children
                    self._remove_empty_nodes(child)

    def _ensure_paragraph_structure(self, article_content: Tag) -> None:
        """Ensure proper paragraph structure in the article.
        
        Wrap text nodes in p tags, etc.
        
        Args:
            article_content: The article content to structure
        """
        # Find all text nodes that are direct children of the article content
        for child in list(article_content.children):
            if child.name is None and child.strip():  # Text node with content
                # Create a new paragraph and replace the text node with it
                p = self.doc.new_tag("p")
                p.string = child.string
                child.replace_with(p)
            elif child.name == "br":
                # Replace br with paragraph if it's a direct child
                p = self.doc.new_tag("p")
                child.replace_with(p)
            elif child.name not in ["p", "div", "article", "section", "h1", "h2", "h3", "h4", "h5", "h6"]:
                # Wrap non-block elements in paragraphs
                if child.name is not None and child.get_text().strip():
                    wrapper = self.doc.new_tag("p")
                    child.wrap(wrapper)

    def _postprocess_content(self, article_content: Tag) -> None:
        """Post-process the article content.
        
        This includes cleaning up the content, fixing links, etc.
        
        Args:
            article_content: The article content to post-process
        """
        if not article_content:
            return
        
        # Fix relative URLs
        self._fix_relative_uris(article_content)
        
        # Clean styles
        self._clean_styles(article_content)
        
        # Clean classes if not preserving them
        if not self.keep_classes:
            self._clean_classes(article_content)
        
        # Clean conditionally
        if self.flags["clean_conditionally"]:
            self._clean_conditionally(article_content, "form")
            self._clean_conditionally(article_content, "table")
            self._clean_conditionally(article_content, "div")
        
        # Clean headers
        self._clean_headers(article_content)
        
        # Prepare the content
        self._prepare_article(article_content)
        
        # Clear readability attributes
        for elem in article_content.find_all(True):
            for attr in list(elem.attrs.keys()):
                if attr.startswith("data-readability-"):
                    del elem[attr]

    def _normalize_attr_value(self, value: Any) -> str:
        """Normalize attribute values that might be lists into strings.
        
        Args:
            value: The attribute value that might be a string or a list
            
        Returns:
            Normalized string value
        """
        if value is None:
            return ""
            
        if isinstance(value, list):
            return " ".join(value)
            
        return str(value).strip()
    
    def _get_inner_text(self, node: Tag, normalize_spaces: bool = True) -> str:
        """Get the inner text of a node.
        
        Args:
            node: The node to get text from
            normalize_spaces: Whether to normalize whitespace
            
        Returns:
            The inner text of the node
        """
        if node is None:
            return ""
        
        # Check cache first
        cache_key = self._get_cache_key(node, f"inner_text:{normalize_spaces}")
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        # Not in cache, compute the value
        text = node.get_text().strip()
        
        if normalize_spaces:
            from readability.utils import normalize_spaces
            text = normalize_spaces(text)
        
        # Store in cache
        self._cache[cache_key] = text
        
        return text

    # DOM Adapter Methods
    
    def _get_element_children(self, node: Tag) -> List[Tag]:
        """Get all element children of a node (excluding text nodes).
        
        Args:
            node: The node to get children from
            
        Returns:
            List of element children
        """
        if not node:
            return []
        return [child for child in node.children if child.name is not None]

    def _get_first_element_child(self, node: Tag) -> Optional[Tag]:
        """Get the first element child of a node (excluding text nodes).
        
        Args:
            node: The node to get first child from
            
        Returns:
            First element child or None
        """
        if not node:
            return None
        for child in node.children:
            if child.name is not None:
                return child
        return None

    def _get_next_element_sibling(self, node: Tag) -> Optional[Tag]:
        """Get the next element sibling of a node (excluding text nodes).
        
        Args:
            node: The node to get next sibling from
            
        Returns:
            Next element sibling or None
        """
        if not node:
            return None
        sibling = node.next_sibling
        while sibling and sibling.name is None:
            sibling = sibling.next_sibling
        return sibling

    def _get_previous_element_sibling(self, node: Tag) -> Optional[Tag]:
        """Get the previous element sibling of a node (excluding text nodes).
        
        Args:
            node: The node to get previous sibling from
            
        Returns:
            Previous element sibling or None
        """
        if not node:
            return None
        sibling = node.previous_sibling
        while sibling and sibling.name is None:
            sibling = sibling.previous_sibling
        return sibling

    def _get_elements_by_tag_name(self, node: Tag, *tag_names: str) -> List[Tag]:
        """Get all elements with specified tag names.
        
        Args:
            node: The node to search in
            *tag_names: Tag names to search for
            
        Returns:
            List of matching elements
        """
        if not node:
            return []
        result = []
        for tag_name in tag_names:
            result.extend(node.find_all(tag_name))
        return result

    def _get_node_ancestors(self, node: Tag, max_depth: int = 0) -> List[Tag]:
        """Get the node's ancestors up to a certain depth.
        
        Args:
            node: The node to get ancestors for
            max_depth: Maximum depth to traverse (0 for unlimited)
            
        Returns:
            List of ancestor nodes
        """
        ancestors = []
        i = 0
        current = node.parent
        
        while current:
            i += 1
            ancestors.append(current)
            if max_depth > 0 and i >= max_depth:
                break
            current = current.parent
            
        return ancestors

    def _get_next_node(self, node: Tag, ignore_self_and_kids: bool = False) -> Optional[Tag]:
        """Get the next node in the document (depth-first traversal).
        
        Args:
            node: The starting node
            ignore_self_and_kids: Whether to skip children of this node
            
        Returns:
            Next node in depth-first order
        """
        if not node:
            return None
            
        # First check for kids if those aren't being ignored
        if not ignore_self_and_kids:
            first_child = self._get_first_element_child(node)
            if first_child:
                return first_child
        
        # Then for siblings
        next_sibling = self._get_next_element_sibling(node)
        if next_sibling:
            return next_sibling
        
        # And finally, move up the parent chain and find a sibling
        current = node
        while current.parent:
            current = current.parent
            next_sibling = self._get_next_element_sibling(current)
            if next_sibling:
                return next_sibling
        
        return None

    def _remove_and_get_next(self, node: Tag) -> Optional[Tag]:
        """Remove a node and get the next node.
        
        Args:
            node: The node to remove
            
        Returns:
            Next node after removal
        """
        next_node = self._get_next_node(node, True)
        if node.parent:
            node.extract()  # BeautifulSoup's remove method
        return next_node

    def _has_ancestor_tag(self, node: Tag, tag: str, max_depth: int = 3, filter_fn: Optional[Callable[[Tag], bool]] = None) -> bool:
        """Check if a node has an ancestor with the given tag.
        
        Args:
            node: The node to check
            tag: Tag name to look for
            max_depth: Maximum depth to check (negative for unlimited)
            filter_fn: Optional filter function for the ancestor
            
        Returns:
            True if node has matching ancestor, False otherwise
        """
        depth = 0
        current = node.parent
        
        while current:
            if max_depth > 0 and depth >= max_depth:
                return False
                
            if current.name == tag and (filter_fn is None or filter_fn(current)):
                return True
                
            current = current.parent
            depth += 1
            
        return False

    def _initialize_node(self, node: Tag) -> None:
        """Initialize a node with readability score.
        
        Also checks the className/id for special names to add to its score.
        
        Args:
            node: The node to initialize
        """
        if not node or not node.name:
            return
            
        # Get base score from class/ID weight
        content_score = float(self._get_class_weight(node))
        
        # Adjust score based on tag name
        tag_name = node.name.lower()
        
        if tag_name == "div":
            content_score += self.SCORE_DIV_TAG
        elif tag_name in ["pre", "td", "blockquote"]:
            content_score += self.SCORE_PRE_TD_BLOCKQUOTE
        elif tag_name in ["address", "ol", "ul", "dl", "dd", "dt", "li", "form"]:
            content_score += self.SCORE_ADDRESS_LIST_FORM
        elif tag_name in ["h1", "h2", "h3", "h4", "h5", "h6", "th"]:
            content_score += self.SCORE_HEADING_TH
        
        # Store the score
        self.score_tracker.set_score(node, content_score)

    def _calculate_content_score(self, node: Tag) -> float:
        """Calculate the content score for a node based on its content.
        
        Args:
            node: The node to score
            
        Returns:
            Content score value
        """
        text = self._get_inner_text(node)
        
        # Check for empty text
        if not text.strip():
            return 0
        
        # Count commas (indicator of prose content)
        comma_count = text.count(',')
        
        # Score: 1 point for the element itself + points for commas + points for length
        score = 1.0 + comma_count + min(math.floor(len(text) / 100), 3)
        
        return score

    def _get_class_weight(self, node: Tag) -> int:
        """Get the class weight for a node based on className/ID.
        
        Args:
            node: The node to get class weight for
            
        Returns:
            Class weight value
        """
        if not self.flags["use_weight_classes"]:
            return 0
        
        weight = 0
        
        # Check for positive/negative classes in className
        class_name = self._normalize_attr_value(node.get("class", []))
        if class_name:
            if re2go.is_positive_class(class_name):
                weight += 25
            if re2go.is_negative_class(class_name):
                weight -= 25
        
        # Check for positive/negative classes in ID
        node_id = self._normalize_attr_value(node.get("id", ""))
        if node_id:
            if re2go.is_positive_class(node_id):
                weight += 25
            if re2go.is_negative_class(node_id):
                weight -= 25
        
        return weight

    def _is_probably_visible(self, node: Tag) -> bool:
        """Determine if a node is likely visible to the user.
        
        Args:
            node: The node to check
            
        Returns:
            True if node is probably visible, False otherwise
        """
        # Check if it's an element
        if not node or not node.name:
            return False
        
        # Check style attribute for display:none or visibility:hidden
        style = node.get('style', '')
        if isinstance(style, list):
            style = " ".join(style)
            
        if RX_DISPLAY_NONE.search(style) or RX_VISIBILITY_HIDDEN.search(style):
            return False
        
        # Check hidden attribute
        if node.has_attr('hidden'):
            return False
        
        # Check aria-hidden attribute
        aria_hidden = node.get('aria-hidden', '')
        if isinstance(aria_hidden, list):
            aria_hidden = " ".join(aria_hidden)
            
        if aria_hidden == 'true':
            # Special case: allow fallback images even with aria-hidden
            class_value = node.get('class', [])
            if isinstance(class_value, list):
                if 'fallback-image' in class_value:
                    return True
            elif class_value == 'fallback-image':
                return True
            return False
        
        return True

    def _get_link_density(self, node: Tag) -> float:
        """Get the link density for a node.
        
        This calculates the ratio of link text to total text in a node.
        A high link density (close to 1.0) indicates the node is likely
        navigation, while a low density indicates content.
        
        Args:
            node: The node to calculate link density for
            
        Returns:
            Link density as a float between 0.0 and 1.0
        """
        # Check cache first
        cache_key = self._get_cache_key(node, "link_density")
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        # Not in cache, compute the value
        text_length = len(self._get_inner_text(node, True))
        if text_length == 0:
            return 0.0
        
        link_length = 0.0
        for link in node.find_all("a"):
            # Links with hash URLs get reduced importance
            href = link.get("href", "")
            coefficient = 0.3 if href and href.startswith("#") else 1.0
            
            # Add up text length in links
            link_text = self._get_inner_text(link, True)
            link_length += len(link_text) * coefficient
        
        # Calculate and cache the result
        result = link_length / text_length
        self._cache[cache_key] = result
        
        return result

    def _clean_styles(self, node: Tag) -> None:
        """Clean styles from a node.
        
        Removes style attributes and deprecated presentational attributes
        from the node and all its descendants.
        
        Args:
            node: The node to clean styles from
        """
        if not node or node.name == "svg":
            return
        
        # List of presentational attributes to remove
        presentational_attrs = [
            "align", "background", "bgcolor", "border", "cellpadding",
            "cellspacing", "frame", "hspace", "rules", "style", "valign", "vspace"
        ]
        
        # List of elements that might have deprecated size attributes
        deprecated_size_elems = ["table", "th", "td", "hr", "pre"]
        
        # Remove presentational attributes
        for attr in presentational_attrs:
            if node.has_attr(attr):
                del node[attr]
        
        # Remove width/height from specific elements
        if node.name in deprecated_size_elems:
            if node.has_attr("width"):
                del node["width"]
            if node.has_attr("height"):
                del node["height"]
        
        # Clean styles from all descendants
        for child in node.find_all(True, recursive=False):
            self._clean_styles(child)

    def _fix_relative_uris(self, node: Tag) -> None:
        """Fix relative URIs in a node.
        
        Converts each <a> and <img> URI in the given element to an absolute URI,
        ignoring #ref URIs.
        
        Args:
            node: The node to fix URIs in
        """
        if not node or not self.document_uri:
            return
        
        # Process links
        for link in node.find_all("a"):
            href = link.get("href", "")
            if isinstance(href, list):
                href = " ".join(href)
                
            if not href:
                continue
            
            # Remove links with javascript: URIs, since they won't
            # work after scripts have been removed from the page
            if href.startswith("javascript:"):
                # If the link only contains simple text content,
                # it can be converted to a text node
                if len(link.contents) == 1 and isinstance(link.contents[0], str):
                    text = self.doc.new_string(link.get_text())
                    link.replace_with(text)
                else:
                    # If the link has multiple children, they should
                    # all be preserved
                    container = self.doc.new_tag("span")
                    for child in list(link.children):
                        container.append(child)
                    link.replace_with(container)
            else:
                # Make URL absolute
                try:
                    abs_url = urljoin(self.document_uri.geturl(), href)
                    link["href"] = abs_url
                except Exception:
                    # If URL conversion fails, remove the href attribute
                    del link["href"]
        
        # Process media elements
        for media in node.find_all(["img", "picture", "figure", "video", "audio", "source"]):
            # Fix src attribute
            src = media.get("src", "")
            if isinstance(src, list):
                src = " ".join(src)
                
            if src:
                try:
                    abs_url = urljoin(self.document_uri.geturl(), src)
                    media["src"] = abs_url
                except Exception:
                    pass
            
            # Fix poster attribute (for video)
            poster = media.get("poster", "")
            if isinstance(poster, list):
                poster = " ".join(poster)
                
            if poster:
                try:
                    abs_url = urljoin(self.document_uri.geturl(), poster)
                    media["poster"] = abs_url
                except Exception:
                    pass
            
            # Fix srcset attribute
            srcset = media.get("srcset", "")
            if isinstance(srcset, list):
                srcset = " ".join(srcset)
                
            if srcset:
                try:
                    # Parse srcset format: "url1 size1, url2 size2, ..."
                    parts = []
                    for src_part in srcset.split(","):
                        src_part = src_part.strip()
                        if not src_part:
                            continue
                        
                        # Split into URL and size
                        space_idx = src_part.rfind(" ")
                        if space_idx == -1:
                            url = src_part
                            size = ""
                        else:
                            url = src_part[:space_idx].strip()
                            size = src_part[space_idx:].strip()
                        
                        # Convert URL to absolute
                        abs_url = urljoin(self.document_uri.geturl(), url)
                        parts.append(f"{abs_url} {size}".strip())
                    
                    # Rebuild srcset
                    media["srcset"] = ", ".join(parts)
                except Exception:
                    pass

    def _validate_encoding(self, doc: BeautifulSoup) -> Optional[str]:
        """Validate that the document encoding was detected properly.
        
        This checks for common signs of encoding problems and returns
        an error message if issues are detected.
        
        Args:
            doc: The BeautifulSoup document
            
        Returns:
            Error message if encoding issues detected, None otherwise
        """
        if not doc:
            return None
            
        # Sample text from document
        sample_text = doc.get_text(strip=True)[:1000]
        
        # Check for telltale signs of encoding issues
        encoding_error_markers = [
            'Ã', 'Â', 'Ð', 'Ñ', 'Ñ', 'Ò', 'Ó', 'Ô', 'Õ', 'Ö', 
            # Common mojibake patterns
            'Ã¢', 'Ã¨', 'Ã©', 'Ã ', 'Ã¹', 'Ã¼', 'Ã¶', 'Ã¤'
        ]
        
        # Count occurrences of error markers
        error_count = sum(sample_text.count(marker) for marker in encoding_error_markers)
        
        # If high concentration of error markers, suggest encoding issue
        if error_count > 10 and error_count / len(sample_text) > 0.05:
            return "Possible encoding issues detected. Try specifying the correct encoding."
        
        return None
        
    def _get_article_favicon(self) -> str:
        """Get the favicon for the article.
        
        Attempts to get high quality favicon that used in article.
        It will only pick favicon in PNG format, so small favicon
        that uses ico file won't be picked.
        """
        from readability.regexps import RX_FAVICON_SIZE
        
        favicon = ""
        favicon_size = -1
        
        # Find all link elements
        link_elements = self.doc.find_all("link")
        
        for link in link_elements:
            # Handle potential AttributeValueList objects
            link_rel = link.get("rel", [])
            if isinstance(link_rel, list):
                link_rel = " ".join(link_rel)
                
            link_type = link.get("type", "")
            if isinstance(link_type, list):
                link_type = " ".join(link_type)
                
            link_href = link.get("href", "")
            if isinstance(link_href, list):
                link_href = " ".join(link_href)
                
            link_sizes = link.get("sizes", "")
            if isinstance(link_sizes, list):
                link_sizes = " ".join(link_sizes)
            
            # Strip whitespace
            link_rel = link_rel.strip() if hasattr(link_rel, "strip") else link_rel
            link_type = link_type.strip() if hasattr(link_type, "strip") else link_type
            link_href = link_href.strip() if hasattr(link_href, "strip") else link_href
            link_sizes = link_sizes.strip() if hasattr(link_sizes, "strip") else link_sizes
            
            if not link_href or "icon" not in link_rel:
                continue
            
            if link_type != "image/png" and not link_href.endswith(".png"):
                continue
            
            size = 0
            for sizes_location in [link_sizes, link_href]:
                match = RX_FAVICON_SIZE.search(sizes_location)
                if match and match.group(1) == match.group(2):
                    size = int(match.group(1))
                    break
            
            if size > favicon_size:
                favicon_size = size
                favicon = link_href
        
        # Make favicon URL absolute
        if favicon and self.document_uri:
            from urllib.parse import urljoin
            favicon = urljoin(self.document_uri.geturl(), favicon)
        
        return favicon
