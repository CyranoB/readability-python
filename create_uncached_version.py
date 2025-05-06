#!/usr/bin/env python
"""
Create an uncached version of the parser.py file.

This script creates a version of parser.py without the caching optimizations
and saves it as parser_backup.py. This allows the compare_performance.py script
to compare the performance of the original and optimized versions.
"""

import os
import re
import shutil


def create_uncached_version():
    """Create an uncached version of the parser.py file."""
    parser_path = os.path.join("readability", "parser.py")
    backup_path = os.path.join("readability", "parser_backup.py")
    
    print(f"Creating uncached version of parser.py at {backup_path}...")
    
    # Read the current parser.py file
    with open(parser_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Remove the _track_cache_stats function
    content = re.sub(
        r"def _track_cache_stats\(self, label: str\) -> None:.*?def _track_memory_usage",
        "def _track_memory_usage",
        content,
        flags=re.DOTALL
    )
    
    # Remove cache checks from _is_probably_visible
    content = re.sub(
        r"# Check cache first\s+cache_key = self\._get_cache_key\(node, \"visibility\"\)\s+if cache_key in self\._cache:\s+return self\._cache\[cache_key\]",
        "",
        content
    )
    
    # Remove cache storage from _is_probably_visible
    content = re.sub(
        r"result = (True|False)\s+self\._cache\[cache_key\] = result\s+return result",
        r"return \1",
        content
    )
    
    # Remove cache checks from _calculate_content_score
    content = re.sub(
        r"# Check cache first\s+cache_key = self\._get_cache_key\(node, \"content_score_calc\"\)\s+if cache_key in self\._cache:\s+return self\._cache\[cache_key\]",
        "",
        content
    )
    
    # Remove cache storage from _calculate_content_score
    content = re.sub(
        r"# Cache the result\s+self\._cache\[cache_key\] = score",
        "",
        content
    )
    
    # Replace the enhanced _has_ancestor_tag with the original version
    content = re.sub(
        r"def _has_ancestor_tag\(self, node: Tag, tag: str, max_depth: int = 3, filter_fn: Optional\[Callable\[\[Tag\], bool\]\] = None\) -> bool:.*?def _has_ancestor_tag_no_cache\(self, node: Tag, tag: str, max_depth: int = 3, filter_fn: Optional\[Callable\[\[Tag\], bool\]\] = None\) -> bool:",
        """def _has_ancestor_tag(self, node: Tag, tag: str, max_depth: int = 3, filter_fn: Optional[Callable[[Tag], bool]] = None) -> bool:
        \"\"\"Check if a node has an ancestor with the given tag.
        
        Args:
            node: The node to check
            tag: Tag name to look for
            max_depth: Maximum depth to check (negative for unlimited)
            filter_fn: Optional filter function for the ancestor
            
        Returns:
            True if node has matching ancestor, False otherwise
        \"\"\"
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
        
    def _has_ancestor_tag_no_cache(self, node: Tag, tag: str, max_depth: int = 3, filter_fn: Optional[Callable[[Tag], bool]] = None) -> bool:""",
        content
    )
    
    # Write the modified content to the backup file
    with open(backup_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"Uncached version created at {backup_path}")


if __name__ == "__main__":
    create_uncached_version()
