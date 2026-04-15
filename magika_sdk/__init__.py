"""
Magika SDK Python - Enhanced AI-powered File Type Detection SDK
================================================================

A comprehensive Python SDK wrapper for Google's Magika AI file type detection,
with enhanced features including async batch processing, enterprise security
strategies, and simplified API for Chinese developers.

Features:
- Simple and intuitive Python API
- Async batch processing with progress bar
- Enterprise security scenario detection strategies
- Multi-language support (output labels in Chinese/English)
- Detailed detection reports with confidence scores

License: MIT
Author: gitstq
Repository: https://github.com/gitstq/magika-sdk-python
"""

__version__ = "1.0.0"
__author__ = "gitstq"
__email__ = "gitstq@github.com"

from .core import MagikaSDK, FileInfo, DetectionResult, DetectionMode
from .async_utils import AsyncMagikaScanner
from .security import SecurityScanner, ThreatLevel, ThreatCategory

__all__ = [
    "__version__",
    "MagikaSDK",
    "FileInfo",
    "DetectionResult",
    "DetectionMode",
    "AsyncMagikaScanner",
    "SecurityScanner",
    "ThreatLevel",
    "ThreatCategory",
]
