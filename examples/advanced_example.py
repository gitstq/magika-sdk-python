#!/usr/bin/env python3
"""
Advanced Usage Examples
=======================

This script demonstrates advanced features of Magika SDK Python package:
- Async batch processing
- Security scanning
- Custom detection modes
- Report generation

Run this script after installing the package:
    pip install magika-sdk-python
    pip install magika

Author: gitstq
License: MIT
"""

import asyncio
import tempfile
import os
from pathlib import Path
from magika_sdk import (
    MagikaSDK,
    AsyncMagikaScanner,
    SecurityScanner,
    DetectionMode,
)


def create_test_directory() -> str:
    """Create a temporary directory with test files."""
    temp_dir = tempfile.mkdtemp()
    
    files = [
        ('script.py', 'print("Python script")'),
        ('data.json', '{"key": "value"}'),
        ('readme.md', '# Documentation'),
        ('style.css', 'body { color: red; }'),
        ('app.js', 'console.log("JavaScript");'),
        ('config.yaml', 'name: test\nversion: 1.0'),
        ('notes.txt', 'Simple text file'),
        ('backup.bat', '@echo off'),
    ]
    
    for filename, content in files:
        filepath = os.path.join(temp_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    return temp_dir


def example_async_scanning():
    """Demonstrate async batch scanning."""
    print("=" * 60)
    print("Example 1: Async Batch Scanning")
    print("=" * 60)
    
    temp_dir = create_test_directory()
    
    try:
        # Initialize async scanner
        scanner = AsyncMagikaScanner(max_workers=10)
        
        # Run async scan
        print(f"Scanning directory: {temp_dir}")
        result = scanner.scan_directory_sync(temp_dir)
        
        print(f"\nResults:")
        print(f"  Total files: {result.total_count}")
        print(f"  Success: {result.success_count}")
        print(f"  Failed: {result.failed_count}")
        
        # Show summary
        summary = result.summary()
        print(f"\nFile type distribution:")
        for label, count in sorted(summary.items(), key=lambda x: -x[1]):
            print(f"  {label}: {count}")
        
        scanner.close()
        print("\nAsync scanning completed!")
        
    finally:
        # Cleanup
        for item in os.listdir(temp_dir):
            os.unlink(os.path.join(temp_dir, item))
        os.rmdir(temp_dir)


def example_security_scanning():
    """Demonstrate security scanning features."""
    print("\n" + "=" * 60)
    print("Example 2: Security Scanning")
    print("=" * 60)
    
    temp_dir = tempfile.mkdtemp()
    
    # Create test files including potentially suspicious ones
    files = [
        ('normal.py', 'print("Normal script")'),
        ('data.json', '{"data": true}'),
        ('backup.bat', '@echo off\ndel /s /q C:\\*'),
        ('malware.exe', b'MZ' + b'\x00' * 100),  # Fake PE header
        ('document.doc', 'This looks like a document'),
    ]
    
    for filename, content in files:
        filepath = os.path.join(temp_dir, filename)
        if isinstance(content, bytes):
            with open(filepath, 'wb') as f:
                f.write(content)
        else:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
    
    try:
        # Initialize security scanner
        scanner = SecurityScanner(check_misnamed=True)
        
        # Run security scan
        print(f"Scanning directory for threats: {temp_dir}")
        report = scanner.scan_directory(temp_dir)
        
        # Show summary
        print(f"\nSecurity Report Summary:")
        print(f"  Total files scanned: {report.total_files}")
        print(f"  Threats found: {len(report.findings)}")
        
        for level in ['critical', 'high', 'medium', 'low']:
            count = report.threat_distribution.get(level, 0)
            if count > 0:
                print(f"  {level.upper()}: {count}")
        
        # Show detailed findings
        if report.findings:
            print(f"\nDetailed Findings:")
            for finding in report.findings[:5]:
                print(f"\n  File: {finding.file_path}")
                print(f"  Threat Level: {finding.threat_level.value}")
                print(f"  Category: {finding.category.value}")
                print(f"  Description: {finding.description}")
                print(f"  Recommendation: {finding.recommendation}")
        
        # Generate text summary
        print(f"\n" + "-" * 40)
        summary_text = scanner.generate_summary(report)
        print(summary_text)
        
    finally:
        # Cleanup
        for item in os.listdir(temp_dir):
            os.unlink(os.path.join(temp_dir, item))
        os.rmdir(temp_dir)


async def example_async_with_progress():
    """Demonstrate async scanning with progress callback."""
    print("\n" + "=" * 60)
    print("Example 3: Async Scanning with Progress")
    print("=" * 60)
    
    temp_dir = create_test_directory()
    
    try:
        scanner = AsyncMagikaScanner(max_workers=5)
        
        completed = [0]
        
        def progress_callback(done: int, total: int):
            completed[0] = done
            print(f"\rProgress: {done}/{total} ({done*100//total}%)", end="", flush=True)
        
        print(f"Scanning with progress tracking...")
        result = await scanner.scan_directory_async(
            temp_dir,
            progress_callback=progress_callback,
        )
        
        print(f"\n\nCompleted! Scanned {result.total_count} files")
        
        scanner.close()
        
    finally:
        # Cleanup
        for item in os.listdir(temp_dir):
            os.unlink(os.path.join(temp_dir, item))
        os.rmdir(temp_dir)


def example_detection_modes():
    """Demonstrate different detection modes."""
    print("\n" + "=" * 60)
    print("Example 4: Detection Modes")
    print("=" * 60)
    
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
    temp_file.write('print("test")')
    temp_file.close()
    
    try:
        modes = [
            DetectionMode.HIGH_CONFIDENCE,
            DetectionMode.MEDIUM_CONFIDENCE,
            DetectionMode.BEST_GUESS,
            DetectionMode.ALL,
        ]
        
        for mode in modes:
            sdk = MagikaSDK(mode=mode)
            result = sdk.detect_file(temp_file.name)
            print(f"Mode: {mode.value:20} -> {result.label} ({result.score:.2%})")
    
    finally:
        os.unlink(temp_file.name)


async def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("Magika SDK Python - Advanced Usage Examples")
    print("=" * 60)
    print()
    
    # Run examples
    example_async_scanning()
    example_security_scanning()
    await example_async_with_progress()
    example_detection_modes()
    
    print("\n" + "=" * 60)
    print("All advanced examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
