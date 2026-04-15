#!/usr/bin/env python3
"""
Setup script for magika-sdk-python
==================================

This setup script handles installation and packaging for the project.

Usage:
    # Install in development mode
    pip install -e .
    
    # Install with all dependencies
    pip install -e ".[dev]"
    
    # Build distribution packages
    python setup.py sdist bdist_wheel
    
    # Upload to PyPI (requires credentials)
    twine upload dist/*

Author: gitstq
License: MIT
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="magika-sdk-python",
    version="1.0.0",
    description="Enhanced Python SDK for AI-powered file type detection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="gitstq",
    author_email="gitstq@github.com",
    url="https://github.com/gitstq/magika-sdk-python",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "magika>=0.1.0",
        "aiofiles>=23.0.0",
        "tqdm>=4.65.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "mypy>=1.0.0",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Filesystems",
    ],
    keywords="file-type detection ai ml security magika",
    project_urls={
        "Bug Reports": "https://github.com/gitstq/magika-sdk-python/issues",
        "Source": "https://github.com/gitstq/magika-sdk-python",
        "Documentation": "https://github.com/gitstq/magika-sdk-python#readme",
    },
)
