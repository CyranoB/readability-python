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
    http_group.add_argument(
        "--encoding", "-e",
        help="Character encoding of the input HTML. Auto-detected if not specified."
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


def fetch_content(url: str, timeout: int = 30, user_agent: Optional[str] = None, 
                 encoding: Optional[str] = None) -> Tuple[Optional[Union[str, bytes]], Optional[str]]:
    """Fetch content from a URL.
    
    Args:
        url: URL to fetch
        timeout: Timeout in seconds
        user_agent: User agent string
        encoding: Optional encoding to use. If specified, content is returned as bytes.
        
    Returns:
        Tuple of (content, error) where content can be str or bytes
    """
    headers = {}
    if user_agent:
        headers["User-Agent"] = user_agent
    
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        
        if encoding:
            # Return raw content as bytes when encoding is specified
            return response.content, None
        else:
            # Let requests handle encoding detection
            return response.text, None
    except requests.RequestException as e:
        return None, f"Error fetching URL: {e}"


def read_file(file_path: str, encoding: Optional[str] = None) -> Tuple[Optional[Union[str, bytes]], Optional[str]]:
    """Read content from a file.
    
    Args:
        file_path: Path to the file
        encoding: Optional encoding to use. If specified, file is read in binary mode
                 and returned as bytes.
        
    Returns:
        Tuple of (content, error) where content can be str or bytes
    """
    try:
        if encoding:
            # Read in binary mode when encoding is specified
            with open(file_path, "rb") as f:
                return f.read(), None
        else:
            # Read in text mode with UTF-8 encoding
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read(), None
    except IOError as e:
        return None, f"Error reading file: {e}"


def read_stdin(encoding: Optional[str] = None) -> Tuple[Optional[Union[str, bytes]], Optional[str]]:
    """Read content from stdin with improved handling.
    
    Detects if stdin is connected to a terminal and provides appropriate
    feedback. Reads in chunks to avoid memory issues with large inputs.
    
    Args:
        encoding: Optional encoding to use. If specified, stdin is read in binary mode
                 and returned as bytes.
    
    Returns:
        Tuple of (content, error) where content can be str or bytes
    """
    # Check if stdin is connected to a terminal
    if sys.stdin.isatty():
        print("Reading from stdin. Enter HTML content and press Ctrl+D (Unix) or Ctrl+Z (Windows) when done:", file=sys.stderr)
    
    try:
        if encoding:
            # Read in binary mode
            stdin_bytes = sys.stdin.buffer.read()
            return stdin_bytes, None
        else:
            # Read with a sensible chunk size to avoid memory issues with very large inputs
            chunks = []
            while True:
                chunk = sys.stdin.read(4096)  # Read in 4KB chunks
                if not chunk:
                    break
                chunks.append(chunk)
                
            return "".join(chunks), None
    except KeyboardInterrupt:
        return None, "Input reading interrupted by user"
    except IOError as e:
        return None, f"Error reading from stdin: {e}"


def process_content(content: Union[str, bytes], url: Optional[str] = None, format: str = "html", 
                   debug: bool = False, encoding: Optional[str] = None) -> Tuple[Optional[str], Optional[str]]:
    """Process content with Readability.
    
    Args:
        content: HTML content to process (string or bytes)
        url: URL for resolving relative links
        format: Output format (html, text, json)
        debug: Enable debug output
        encoding: Optional character encoding to use when content is bytes
        
    Returns:
        Tuple of (processed_content, error)
    """
    if debug:
        print(f"Processing content with URL: {url}", file=sys.stderr)
        if encoding:
            print(f"Using encoding: {encoding}", file=sys.stderr)
    
    parser = Readability(debug=debug)
    article, error = parser.parse(content, url=url, encoding=encoding)
    
    if error:
        return None, f"Error parsing content: {error}"
    
    if not article:
        return None, "No article content found"
    
    if format == "html":
        # Wrap the content in a proper HTML document structure with encoding declaration
        html_document = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>{article.title or "Extracted Content"}</title>
</head>
<body>
    {article.content}
</body>
</html>"""
        return html_document, None
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


# Define error code constants
EXIT_SUCCESS = 0
EXIT_ERROR_INPUT = 1
EXIT_ERROR_NETWORK = 2  
EXIT_ERROR_PARSING = 3
EXIT_ERROR_OUTPUT = 4
EXIT_ERROR_UNKNOWN = 10

def main() -> int:
    """Main entry point for the CLI with improved error handling.
    
    Returns:
        Exit code based on specific error types
    """
    args = parse_args()
    
    try:
        # Get content from URL, file, or stdin
        content = None
        error = None
        url = args.url
        
        if args.input:
            if args.input.startswith(("http://", "https://")):
                try:
                    # Input is a URL
                    content, error = fetch_content(args.input, args.timeout, args.user_agent, args.encoding)
                    if error:
                        print(f"Network error: {error}", file=sys.stderr)
                        return EXIT_ERROR_NETWORK
                    if not url:
                        url = args.input
                except requests.RequestException as e:
                    print(f"Network error: {e}", file=sys.stderr)
                    return EXIT_ERROR_NETWORK
            else:
                try:
                    # Input is a file
                    content, error = read_file(args.input, args.encoding)
                    if error:
                        print(f"File error: {error}", file=sys.stderr)
                        return EXIT_ERROR_INPUT
                except FileNotFoundError:
                    print(f"Error: File not found: {args.input}", file=sys.stderr)
                    return EXIT_ERROR_INPUT
                except PermissionError:
                    print(f"Error: Permission denied for file: {args.input}", file=sys.stderr)
                    return EXIT_ERROR_INPUT
        else:
            # Input from stdin
            content, error = read_stdin(args.encoding)
            if error:
                print(f"Input error: {error}", file=sys.stderr)
                return EXIT_ERROR_INPUT
        
        if not content:
            print("Error: No content to process", file=sys.stderr)
            return EXIT_ERROR_INPUT
        
        # Process content
        try:
            processed_content, error = process_content(content, url, args.format, args.debug, args.encoding)
            
            if error:
                print(f"Error parsing content: {error}", file=sys.stderr)
                return EXIT_ERROR_PARSING
            
            if not processed_content:
                print("Error: No content extracted", file=sys.stderr)
                return EXIT_ERROR_PARSING
        except Exception as e:
            print(f"Unexpected error during content processing: {e}", file=sys.stderr)
            return EXIT_ERROR_PARSING
        
        # Write output
        try:
            success, error = write_output(processed_content, args.output)
            
            if not success:
                print(f"Error writing output: {error}", file=sys.stderr)
                return EXIT_ERROR_OUTPUT
        except Exception as e:
            print(f"Unexpected error writing output: {e}", file=sys.stderr)
            return EXIT_ERROR_OUTPUT
        
        return EXIT_SUCCESS
    except KeyboardInterrupt:
        print("\nOperation interrupted by user", file=sys.stderr)
        return EXIT_ERROR_UNKNOWN
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return EXIT_ERROR_UNKNOWN


if __name__ == "__main__":
    sys.exit(main())
