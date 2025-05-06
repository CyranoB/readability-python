"""Memory usage test for Readability parser."""

import os
import sys
from memory_profiler import profile
from readability import Readability

def generate_large_html(size_mb=10):
    """Generate a large HTML document of approximately the given size in MB."""
    # Calculate how many divs we need to reach the target size
    # Each div is about 1KB
    n_divs = size_mb * 1000
    
    html_start = "<html><body>"
    html_end = "</body></html>"
    div_template = "<div><p>" + "x" * 1000 + "</p></div>"
    
    html = html_start + div_template * n_divs + html_end
    return html

@profile
def test_memory_usage():
    """Test memory usage of the Readability parser."""
    print("Generating large HTML document...")
    html = generate_large_html(2)  # 2MB HTML
    
    print(f"HTML size: {len(html) / 1024 / 1024:.2f}MB")
    
    print("Parsing document...")
    parser = Readability(debug=True)
    article, error = parser.parse(html)
    
    print("Parsing complete.")
    if error:
        print(f"Error: {error}")
    else:
        print(f"Article length: {article.length}")
    
    # Force garbage collection
    import gc
    gc.collect()
    
    return article

if __name__ == "__main__":
    test_memory_usage()
