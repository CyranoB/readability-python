#!/usr/bin/env python
"""
Compare performance between original and optimized versions of Python Readability.

This script compares the performance of the original parser.py (without caching optimizations)
against the optimized version (with caching). It uses the benchmark.py script to run
the benchmarks and reports the performance differences.

Usage:
    python compare_performance.py [--profile] [--memory] [--verbose] [--repeat N] [file1.html file2.html ...]

Options:
    --profile       Enable detailed profiling with cProfile
    --memory        Track memory usage (requires psutil)
    --verbose       Print detailed information during benchmarking
    --repeat N      Repeat each benchmark N times (default: 3)
    
If no files are specified, the script will use test files from the test-pages directory.
"""

import os
import sys
import shutil
import argparse
import subprocess
import tempfile
from typing import List, Dict, Any, Tuple

# Import the benchmark module
import benchmark


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Compare performance between original and optimized versions")
    parser.add_argument("files", nargs="*", help="HTML files to benchmark")
    parser.add_argument("--profile", action="store_true", help="Enable detailed profiling")
    parser.add_argument("--memory", action="store_true", help="Track memory usage")
    parser.add_argument("--verbose", action="store_true", help="Print detailed information")
    parser.add_argument("--repeat", type=int, default=3, help="Repeat each benchmark N times")
    return parser.parse_args()


def backup_parser() -> str:
    """Create a backup of the current parser.py file.
    
    Returns:
        Path to the backup file
    """
    parser_path = os.path.join("readability", "parser.py")
    backup_path = os.path.join(tempfile.gettempdir(), "parser_backup.py")
    
    print(f"Backing up current parser.py to {backup_path}...")
    shutil.copy2(parser_path, backup_path)
    
    return backup_path


def restore_original_parser() -> None:
    """Restore the original parser.py file (without caching optimizations)."""
    parser_path = os.path.join("readability", "parser.py")
    backup_path = os.path.join("readability", "parser_backup.py")
    
    if not os.path.exists(backup_path):
        print("Error: Original parser backup not found at readability/parser_backup.py")
        print("Please ensure you have a backup of the original parser before running this script.")
        sys.exit(1)
    
    print("Restoring original parser.py (without caching optimizations)...")
    shutil.copy2(backup_path, parser_path)


def restore_optimized_parser(backup_path: str) -> None:
    """Restore the optimized parser.py file (with caching optimizations).
    
    Args:
        backup_path: Path to the backup of the optimized parser
    """
    parser_path = os.path.join("readability", "parser.py")
    
    print("Restoring optimized parser.py (with caching optimizations)...")
    shutil.copy2(backup_path, parser_path)


def run_benchmarks(args: argparse.Namespace, version_name: str) -> List[Dict[str, Any]]:
    """Run benchmarks using the benchmark.py script.
    
    Args:
        args: Command line arguments
        version_name: Name of the version being benchmarked
        
    Returns:
        List of benchmark results
    """
    print(f"\nRunning benchmarks for {version_name} version...")
    
    # Get test files
    test_files = benchmark.get_test_files(args.files)
    
    if not test_files:
        print("No test files found.")
        return []
    
    # Run benchmarks
    results = []
    for i, file_path in enumerate(test_files):
        print(f"[{i+1}/{len(test_files)}] Benchmarking {file_path}...")
        
        result = benchmark.benchmark_file(
            file_path, 
            profile=args.profile,
            track_memory=args.memory,
            verbose=args.verbose,
            repeat=args.repeat
        )
        
        # Add version name to result
        result["version"] = version_name
        
        results.append(result)
        
        # Print summary for this file
        print(f"  Average time: {result['avg_time']:.4f} seconds")
        if args.memory:
            print(f"  Memory usage: {result['memory_diff']:.2f} MB")
        
        print()
    
    return results


def compare_results(original_results: List[Dict[str, Any]], optimized_results: List[Dict[str, Any]]) -> None:
    """Compare benchmark results between original and optimized versions.
    
    Args:
        original_results: Benchmark results for the original version
        optimized_results: Benchmark results for the optimized version
    """
    if not original_results or not optimized_results:
        print("No results to compare.")
        return
    
    # Ensure both result lists have the same files in the same order
    original_files = [result["file"] for result in original_results]
    optimized_files = [result["file"] for result in optimized_results]
    
    if original_files != optimized_files:
        print("Warning: Files in original and optimized results don't match.")
        return
    
    print("=" * 100)
    print("Performance Comparison: Original vs. Optimized")
    print("=" * 100)
    print(f"{'File':<30} {'Original Time (s)':<15} {'Optimized Time (s)':<15} {'Improvement':<15} {'Speedup':<10}")
    print("-" * 100)
    
    total_original_time = 0.0
    total_optimized_time = 0.0
    
    for i in range(len(original_results)):
        original = original_results[i]
        optimized = optimized_results[i]
        
        file_name = os.path.basename(original["file"])
        original_time = original["avg_time"]
        optimized_time = optimized["avg_time"]
        
        improvement = original_time - optimized_time
        improvement_percent = (improvement / original_time) * 100 if original_time > 0 else 0
        speedup = original_time / optimized_time if optimized_time > 0 else 0
        
        print(f"{file_name:<30} {original_time:<15.4f} {optimized_time:<15.4f} {improvement_percent:<14.2f}% {speedup:<10.2f}x")
        
        total_original_time += original_time
        total_optimized_time += optimized_time
    
    print("-" * 100)
    
    # Calculate overall improvement
    total_improvement = total_original_time - total_optimized_time
    total_improvement_percent = (total_improvement / total_original_time) * 100 if total_original_time > 0 else 0
    total_speedup = total_original_time / total_optimized_time if total_optimized_time > 0 else 0
    
    print(f"{'Total':<30} {total_original_time:<15.4f} {total_optimized_time:<15.4f} {total_improvement_percent:<14.2f}% {total_speedup:<10.2f}x")
    print("=" * 100)
    
    # Print memory comparison if available
    if "memory_diff" in original_results[0] and "memory_diff" in optimized_results[0]:
        print("\nMemory Usage Comparison (MB)")
        print("=" * 100)
        print(f"{'File':<30} {'Original':<15} {'Optimized':<15} {'Difference':<15} {'Improvement':<10}")
        print("-" * 100)
        
        total_original_memory = 0.0
        total_optimized_memory = 0.0
        
        for i in range(len(original_results)):
            original = original_results[i]
            optimized = optimized_results[i]
            
            file_name = os.path.basename(original["file"])
            original_memory = original["memory_diff"]
            optimized_memory = optimized["memory_diff"]
            
            memory_diff = original_memory - optimized_memory
            memory_percent = (memory_diff / original_memory) * 100 if original_memory > 0 else 0
            
            print(f"{file_name:<30} {original_memory:<15.2f} {optimized_memory:<15.2f} {memory_diff:<15.2f} {memory_percent:<10.2f}%")
            
            total_original_memory += original_memory
            total_optimized_memory += optimized_memory
        
        print("-" * 100)
        
        # Calculate overall memory improvement
        total_memory_diff = total_original_memory - total_optimized_memory
        total_memory_percent = (total_memory_diff / total_original_memory) * 100 if total_original_memory > 0 else 0
        
        print(f"{'Total':<30} {total_original_memory:<15.2f} {total_optimized_memory:<15.2f} {total_memory_diff:<15.2f} {total_memory_percent:<10.2f}%")
        print("=" * 100)


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
    
    # Backup current parser.py (optimized version)
    optimized_backup = backup_parser()
    
    try:
        # Restore original parser.py (without caching)
        restore_original_parser()
        
        # Run benchmarks on original version
        original_results = run_benchmarks(args, "Original")
        
        # Restore optimized parser.py (with caching)
        restore_optimized_parser(optimized_backup)
        
        # Run benchmarks on optimized version
        optimized_results = run_benchmarks(args, "Optimized")
        
        # Compare results
        compare_results(original_results, optimized_results)
        
    finally:
        # Always restore the optimized version
        restore_optimized_parser(optimized_backup)
        
        # Clean up backup
        if os.path.exists(optimized_backup):
            os.remove(optimized_backup)


if __name__ == "__main__":
    main()
