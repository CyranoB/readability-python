"""Tests for memory management improvements in the Readability parser."""

import pytest
from bs4 import BeautifulSoup
from readability import Readability
from readability.parser import ScoreTracker


def test_score_tracker_clear_unused():
    """Test clearing unused scores from ScoreTracker."""
    tracker = ScoreTracker()
    soup = BeautifulSoup("<div><p>1</p><p>2</p><p>3</p></div>", "lxml")
    
    div = soup.div
    p1, p2, p3 = div.find_all("p")
    
    # Set scores
    tracker.set_score(div, 10)
    tracker.set_score(p1, 1)
    tracker.set_score(p2, 2)
    tracker.set_score(p3, 3)
    
    # Verify initial state
    assert len(tracker.get_scored_nodes()) == 4
    
    # Clear unused (keep div and p1)
    cleared = tracker.clear_unused_scores([div, p1])
    
    # Verify
    assert cleared == 2
    assert tracker.has_score(div)
    assert tracker.has_score(p1)
    assert not tracker.has_score(p2)
    assert not tracker.has_score(p3)


def test_clear_cache_section():
    """Test clearing specific sections of the cache."""
    parser = Readability()
    soup = BeautifulSoup("<div><p>Test</p></div>", "lxml")
    
    # Add some cache entries
    parser._cache = {
        "123:inner_text:true": "text1",
        "456:inner_text:false": "text2",
        "789:link_density": 0.5,
        "101:other": "value"
    }
    
    # Clear inner_text section
    cleared = parser._clear_cache_section("inner_text")
    
    # Verify
    assert cleared == 2
    assert len(parser._cache) == 2
    assert "789:link_density" in parser._cache
    assert "101:other" in parser._cache
    assert "123:inner_text:true" not in parser._cache
    assert "456:inner_text:false" not in parser._cache


def test_release_resources():
    """Test releasing resources after parsing."""
    parser = Readability()
    
    # Set up some state
    parser._cache = {"key": "value"}
    parser.doc = BeautifulSoup("<html><body><p>Test</p></body></html>", "lxml")
    
    # Mock the score tracker
    class MockScoreTracker:
        def __init__(self):
            self.cleared = False
            
        def clear(self):
            self.cleared = True
    
    mock_tracker = MockScoreTracker()
    parser.score_tracker = mock_tracker
    
    # Release resources
    parser._release_resources()
    
    # Verify
    assert len(parser._cache) == 0
    assert parser.doc is None
    assert mock_tracker.cleared


def test_memory_management_large_document():
    """Test memory management with large document."""
    # Create a large HTML document
    large_html = "<html><body>" + "<div><p>" + "x" * 1000 + "</p></div>" * 500 + "</body></html>"
    
    # Parse document
    parser = Readability(debug=True)
    article, error = parser.parse(large_html)
    
    # Verify we got an article and no error
    assert error is None
    assert article is not None
    
    # Verify parser resources were released
    assert parser.doc is None
    assert len(parser._cache) == 0


@pytest.mark.parametrize("test_case", ["001", "nytimes-1", "mozilla-1"])
def test_memory_management_real_pages(test_case):
    """Test memory management with real-world pages."""
    import os
    import json
    from pathlib import Path
    
    # Get test data directly
    base_dir = Path("tests") / "test-pages" / test_case
    
    # Skip if directory doesn't exist
    if not base_dir.exists():
        pytest.skip(f"Test directory {base_dir} not found")
    
    # Load source HTML
    source_path = base_dir / "source.html"
    if not source_path.exists():
        pytest.skip(f"Source file not found in {base_dir}")
        
    with open(source_path, "r", encoding="utf-8") as f:
        source_html = f.read()
    
    # Create mock URL
    url = f"https://example.com/test-pages/{test_case}"
    
    # Parse with memory tracking
    parser = Readability(debug=True)
    article, error = parser.parse(source_html, url=url)
    
    # Verify
    assert error is None
    assert article is not None
    assert parser.doc is None
    assert len(parser._cache) == 0


def test_get_inner_text_caching():
    """Test that _get_inner_text only caches large nodes."""
    parser = Readability()
    
    # Create a small node
    small_soup = BeautifulSoup("<p>Small node</p>", "lxml")
    small_node = small_soup.p
    
    # Create a large node
    large_html = "<div>" + "<p>Paragraph</p>" * 20 + "</div>"
    large_soup = BeautifulSoup(large_html, "lxml")
    large_node = large_soup.div
    
    # Clear cache
    parser._cache = {}
    
    # Get inner text for small node
    small_text = parser._get_inner_text(small_node)
    
    # Verify small node text is not cached
    assert len(parser._cache) == 0
    
    # Get inner text for large node
    large_text = parser._get_inner_text(large_node)
    
    # Verify large node text is cached
    assert len(parser._cache) == 1
    
    # Get the cache key
    cache_key = next(iter(parser._cache.keys()))
    
    # Verify the cached value
    assert parser._cache[cache_key] == large_text


def test_grab_article_memory_management():
    """Test memory management in _grab_article method."""
    # Create HTML with multiple candidates
    html = """
    <html>
    <body>
        <div id="content">
            <p>This is a paragraph with enough text to be considered for scoring.
            It has multiple sentences and commas, which should give it a good score.
            We want to make sure it's long enough to be counted.</p>
            <p>Another paragraph with enough text to be considered for scoring.
            It also has multiple sentences and commas, for a good score.
            We need to ensure it's long enough to be counted as well.</p>
        </div>
        <div id="sidebar">
            <p>Short sidebar text.</p>
            <ul>
                <li>Menu item 1</li>
                <li>Menu item 2</li>
            </ul>
        </div>
    </body>
    </html>
    """
    
    # Create parser
    parser = Readability(debug=True)
    
    # Parse HTML
    parser.doc = BeautifulSoup(html, "lxml")
    
    # Call _grab_article directly
    article_content = parser._grab_article()
    
    # Verify article content was extracted
    assert article_content is not None
    
    # Verify score tracker has limited entries
    # Only the top candidate and its ancestors should have scores
    assert len(parser.score_tracker.get_scored_nodes()) <= 5  # div#content + body + html + maybe 1-2 others
