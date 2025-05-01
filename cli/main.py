#!/usr/bin/env python3
"""Command-line interface for Python Readability."""

import argparse
import json
import sys
import requests
from typing import Optional, Tuple, Dict, Any, Union
from pathlib import Path

from readability import Readability, Article


def parse_args() -> argparse.Namespace:
    """Parse command line arguments.
    
    Returns:
        Parsed command line arguments
    """
    parser = argparse.ArgumentParser(
        description="Extract the main content from HTML pages.",
        prog="readability-python"
    )
    
    # Input options
    input_group = parser.add_argument_group("Input options")
    input_group.add_argument(
        "input",
        nargs="?",
        help="URL or file path to process. If not provided, reads from stdin."
    )
    input_group.add_argument(
        "--url",
        help="Explicitly specify the URL for resolving relative links."
    )
    
    # Output options
    output_group = parser.add_argument_group("Output options")
    output_group.add_argument(
        "--output", "-o",
        help="Output file path. If not provided, writes to stdout."
    )
    output_group.add_argument(
        "--format", "-f",
        choices=["html", "text", "json"],
        default="html",
        help="Output format. Default: html"
    )
    
    # HTTP options
    http_group = parser.add_argument_group("HTTP options")
    http_group.add_argument(
        "--user-agent", "-u",
        help="User agent for HTTP requests."
    )
    http_group.add_argument(
        "--timeout", "-t",
        type=int,
        default=30,
        help="Timeout for HTTP requests in seconds. Default: 30"
    )
    
    # Other options
    parser.add_argument(
        "--debug", "-d",
        action="store_true",
        help="Enable debug output."
    )
    parser.add_argument(
        "--version", "-v",
        action="version",
        version=f"%(prog)s {__import__('cli').__version__}"
    )
    
    return parser.parse_args()


def fetch_content(url: str, timeout: int = 30, user_agent: Optional[str] = None) -> Tuple[Optional[str], Optional[str]]:
    """Fetch content from a URL.
    
    Args:
        url: URL to fetch
        timeout: Timeout in seconds
        user_agent: User agent string
        
    Returns:
        Tuple of (content, error)
    """
    headers = {}
    if user_agent:
        headers["User-Agent"] = user_agent
    
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.text, None
    except requests.RequestException as e:
        return None, f"Error fetching URL: {e}"


def read_file(file_path: str) -> Tuple[Optional[str], Optional[str]]:
    """Read content from a file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Tuple of (content, error)
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read(), None
    except IOError as e:
        return None, f"Error reading file: {e}"


def read_stdin() -> Tuple[Optional[str], Optional[str]]:
    """Read content from stdin.
    
    Returns:
        Tuple of (content, error)
    """
    try:
        return sys.stdin.read(), None
    except IOError as e:
        return None, f"Error reading from stdin: {e}"


def process_content(content: str, url: Optional[str] = None, format: str = "html", debug: bool = False) -> Tuple[Optional[str], Optional[str]]:
    """Process content with Readability.
    
    Args:
        content: HTML content to process
        url: URL for resolving relative links
        format: Output format (html, text, json)
        debug: Enable debug output
        
    Returns:
        Tuple of (processed_content, error)
    """
    if debug:
        print(f"Processing content with URL: {url}", file=sys.stderr)
    
    parser = Readability()
    article, error = parser.parse(content, url=url)
    
    if error:
        return None, f"Error parsing content: {error}"
    
    if not article:
        return None, "No article content found"
    
    if format == "html":
        return article.content, None
    elif format == "text":
        return article.text_content, None
    elif format == "json":
        article_dict = {
            "title": article.title,
            "byline": article.byline,
            "content": article.content,
            "text_content": article.text_content,
            "excerpt": article.excerpt,
            "site_name": article.site_name,
            "image": article.image,
            "favicon": article.favicon,
            "length": article.length,
            "published_time": article.published_time.isoformat() if article.published_time else None,
            "url": article.url
        }
        return json.dumps(article_dict, indent=2), None
    else:
        return None, f"Unknown format: {format}"


def write_output(content: str, output_path: Optional[str] = None) -> Tuple[bool, Optional[str]]:
    """Write content to output destination.
    
    Args:
        content: Content to write
        output_path: Path to output file, or None for stdout
        
    Returns:
        Tuple of (success, error)
    """
    if output_path:
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(content)
            return True, None
        except IOError as e:
            return False, f"Error writing to file: {e}"
    else:
        try:
            print(content)
            return True, None
        except IOError as e:
            return False, f"Error writing to stdout: {e}"


def main() -> int:
    """Main entry point for the CLI.
    
    Returns:
        Exit code
    """
    args = parse_args()
    
    # Get content from URL, file, or stdin
    content = None
    error = None
    url = args.url
    
    if args.input:
        if args.input.startswith(("http://", "https://")):
            # Input is a URL
            content, error = fetch_content(args.input, args.timeout, args.user_agent)
            if not url:
                url = args.input
        else:
            # Input is a file
            content, error = read_file(args.input)
    else:
        # Input from stdin
        content, error = read_stdin()
    
    if error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    
    if not content:
        print("Error: No content to process", file=sys.stderr)
        return 1
    
    # Process content
    processed_content, error = process_content(content, url, args.format, args.debug)
    
    if error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    
    if not processed_content:
        print("Error: No content extracted", file=sys.stderr)
        return 1
    
    # Write output
    success, error = write_output(processed_content, args.output)
    
    if not success:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
