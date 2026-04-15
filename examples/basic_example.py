#!/usr/bin/env python3
"""
Basic Usage Examples
====================

This script demonstrates the basic usage of Magika SDK Python package.

Run this script after installing the package:
    pip install magika-sdk-python
    pip install magika

Author: gitstq
License: MIT
"""

from pathlib import Path
from magika_sdk import MagikaSDK, DetectionMode


def main():
    print("=" * 60)
    print("Magika SDK Python - Basic Usage Examples")
    print("=" * 60)
    print()
    
    # Initialize SDK
    print("1. Initializing Magika SDK...")
    sdk = MagikaSDK(mode=DetectionMode.BEST_GUESS)
    print("   SDK initialized successfully!")
    print()
    
    # Example 1: Detect file type from path
    print("2. Detecting single file type...")
    # Test with a Python file
    sample_code = '''
def hello():
    print("Hello, World!")
'''
    
    # Create temporary test file
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(sample_code)
        temp_file = f.name
    
    try:
        result = sdk.detect_file(temp_file)
        print(f"   File: {temp_file}")
        print(f"   Label: {result.label}")
        print(f"   Description: {result.description}")
        print(f"   MIME Type: {result.mime_type}")
        print(f"   Confidence: {result.score:.2%}")
        print(f"   Is Text: {result.is_text}")
    finally:
        import os
        os.unlink(temp_file)
    
    print()
    
    # Example 2: Detect from bytes
    print("3. Detecting file type from bytes...")
    python_bytes = b'print("Hello from bytes")'
    result = sdk.detect_bytes(python_bytes, path="sample.py")
    print(f"   Bytes content type: {result.label}")
    print(f"   Description: {result.description}")
    print()
    
    # Example 3: Get supported types
    print("4. Supported file types (sample):")
    supported = sdk.get_supported_types()
    for item in supported[:10]:
        print(f"   - {item['label']}: {item['description']}")
    print(f"   ... and more ({len(supported)} total types)")
    print()
    
    # Example 4: Batch scanning with directory
    print("5. Batch scanning demonstration...")
    print("   Note: For actual directory scanning, use scan_directory() method")
    print("   Example:")
    print('   result = sdk.scan_directory("./my_folder")')
    print('   for file in result.files:')
    print('       print(f"{file.path}: {file.label}")')
    print()
    
    print("=" * 60)
    print("Basic examples completed!")
    print("See advanced_example.py for more features.")


if __name__ == "__main__":
    main()
