#!/usr/bin/env python
"""
Benchmark script for Python Readability.

This script benchmarks the performance of the Readability parser on various HTML files.
It measures execution time, memory usage, and provides profiling information to identify bottlenecks.

Usage:
    python benchmark.py [--profile] [--memory] [--verbose] [--repeat N] [file1.html file2.html ...]

Options:
    --profile       Enable detailed profiling with cProfile
    --memory        Track memory usage (requires psutil)
    --verbose       Print detailed information during benchmarking
    --repeat N      Repeat each benchmark N times (default: 3)
    
If no files are specified, the script will use test files from the test-pages directory.
"""

import os
import sys
import time
import argparse
import cProfile
import pstats
import io
import gc
from pathlib import Path
from typing import List, Tuple, Dict, Any, Optional

# Add the project root to the path so we can import the readability module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from readability import Readability


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Benchmark Python Readability")
    parser.add_argument("files", nargs="*", help="HTML files to benchmark")
    parser.add_argument("--profile", action="store_true", help="Enable detailed profiling")
    parser.add_argument("--memory", action="store_true", help="Track memory usage")
    parser.add_argument("--verbose", action="store_true", help="Print detailed information")
    parser.add_argument("--repeat", type=int, default=3, help="Repeat each benchmark N times")
    return parser.parse_args()


def get_test_files(specified_files: List[str] = None) -> List[str]:
    """Get a list of HTML files to benchmark.
    
    If specified_files is provided, use those files.
    Otherwise, use test files from the test-pages directory.
    """
    if specified_files:
        return specified_files
    
    # Use test files from the test-pages directory
    test_dirs = [
        "tests/test-pages/001",
        "tests/test-pages/medium-1",
        "tests/test-pages/nytimes-1",
        "tests/test-pages/bbc-1",
        "tests/test-pages/wikipedia"
    ]
    
    test_files = []
    for test_dir in test_dirs:
        if os.path.exists(test_dir):
            source_file = os.path.join(test_dir, "source.html")
            if os.path.exists(source_file):
                test_files.append(source_file)
    
    return test_files


def get_memory_usage() -> float:
    """Get current memory usage in MB."""
    try:
        import psutil
        process = psutil.Process()
        return process.memory_info().rss / 1024 / 1024
    except ImportError:
        print("Warning: psutil not installed. Memory tracking disabled.")
        return 0.0


def benchmark_file(file_path: str, profile: bool = False, track_memory: bool = False, 
                  verbose: bool = False, repeat: int = 3) -> Dict[str, Any]:
    """Benchmark parsing a single HTML file."""
    # Read the file
    with open(file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    file_size = len(html_content) / 1024  # KB
    
    # Initialize results
    results = {
        "file": file_path,
        "size_kb": file_size,
        "times": [],
        "avg_time": 0.0,
        "memory_before": 0.0,
        "memory_after": 0.0,
        "memory_diff": 0.0,
        "profile_stats": None
    }
    
    # Force garbage collection before benchmarking
    gc.collect()
    
    # Track memory before parsing
    if track_memory:
        results["memory_before"] = get_memory_usage()
    
    # Run the benchmark multiple times
    for i in range(repeat):
        if verbose:
            print(f"  Run {i+1}/{repeat}...")
        
        # Create a new parser for each run
        parser = Readability()
        
        if profile and i == 0:  # Only profile the first run
            # Profile the parsing
            pr = cProfile.Profile()
            pr.enable()
            
            start_time = time.time()
            article, error = parser.parse(html_content)
            elapsed = time.time() - start_time
            
            pr.disable()
            
            # Save profiling results
            s = io.StringIO()
            ps = pstats.Stats(pr, stream=s).sort_stats("cumulative")
            ps.print_stats(20)  # Print top 20 time-consuming functions
            results["profile_stats"] = s.getvalue()
        else:
            # Just measure time
            start_time = time.time()
            article, error = parser.parse(html_content)
            elapsed = time.time() - start_time
        
        results["times"].append(elapsed)
        
        if error:
            print(f"Error parsing {file_path}: {error}")
    
    # Calculate average time
    results["avg_time"] = sum(results["times"]) / len(results["times"])
    
    # Track memory after parsing
    if track_memory:
        # Force garbage collection to get accurate memory usage
        gc.collect()
        results["memory_after"] = get_memory_usage()
        results["memory_diff"] = results["memory_after"] - results["memory_before"]
    
    return results


def run_benchmarks(args: argparse.Namespace) -> List[Dict[str, Any]]:
    """Run benchmarks on all specified files."""
    test_files = get_test_files(args.files)
    
    if not test_files:
        print("No test files found.")
        return []
    
    print(f"Benchmarking {len(test_files)} files...")
    
    results = []
    for i, file_path in enumerate(test_files):
        print(f"[{i+1}/{len(test_files)}] Benchmarking {file_path}...")
        
        result = benchmark_file(
            file_path, 
            profile=args.profile,
            track_memory=args.memory,
            verbose=args.verbose,
            repeat=args.repeat
        )
        
        results.append(result)
        
        # Print summary for this file
        print(f"  Average time: {result['avg_time']:.4f} seconds")
        if args.memory:
            print(f"  Memory usage: {result['memory_diff']:.2f} MB")
        
        # Print profiling information if requested
        if args.profile and args.verbose and result["profile_stats"]:
            print("\nProfiling information:")
            print(result["profile_stats"])
        
        print()
    
    return results


def print_summary(results: List[Dict[str, Any]]) -> None:
    """Print a summary of all benchmark results."""
    if not results:
        return
    
    print("=" * 80)
    print("Benchmark Summary")
    print("=" * 80)
    print(f"{'File':<40} {'Size (KB)':<10} {'Avg Time (s)':<15} {'Memory (MB)':<10}")
    print("-" * 80)
    
    total_time = 0.0
    total_memory = 0.0
    
    for result in results:
        file_name = os.path.basename(result["file"])
        print(f"{file_name:<40} {result['size_kb']:<10.2f} {result['avg_time']:<15.4f} {result['memory_diff']:<10.2f}")
        total_time += result["avg_time"]
        total_memory += result["memory_diff"]
    
    print("-" * 80)
    print(f"{'Total':<40} {'':<10} {total_time:<15.4f} {total_memory:<10.2f}")
    print("=" * 80)


def main() -> None:
    """Main function."""
    args = parse_args()
    
    # Check if psutil is installed for memory tracking
    if args.memory:
        try:
            import psutil
        except ImportError:
            print("Warning: psutil not installed. Memory tracking disabled.")
            args.memory = False
    
    # Run benchmarks
    results = run_benchmarks(args)
    
    # Print summary
    print_summary(results)


if __name__ == "__main__":
    main()
