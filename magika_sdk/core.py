"""
Magika SDK Core Module
======================

Core functionality for AI-powered file type detection.
Provides a simplified and enhanced API for Google's Magika.

Author: gitstq
License: MIT
"""

import os
import json
from pathlib import Path
from typing import Optional, Union, List, Dict, Any
from dataclasses import dataclass, field
from enum import Enum
from functools import lru_cache

try:
    from magika import Magika as MagikaCore
    from magika.tool.magika import Magika as MagikaCLI
    from magika.types import MagikaResult
    MAGIKA_AVAILABLE = True
except ImportError:
    MAGIKA_AVAILABLE = False
    MagikaCore = None
    MagikaCLI = None


class DetectionMode(Enum):
    """Detection mode options with confidence levels."""
    HIGH_CONFIDENCE = "high"      # Only return high confidence results
    MEDIUM_CONFIDENCE = "medium"  # Include medium confidence results
    BEST_GUESS = "best"           # Always return best guess
    ALL = "all"                   # Return all possible results


@dataclass
class FileInfo:
    """Information about a detected file."""
    path: str
    label: str
    description: str
    mime_type: str
    is_text: bool
    group: str
    score: float
    extensions: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "path": self.path,
            "label": self.label,
            "description": self.description,
            "mime_type": self.mime_type,
            "is_text": self.is_text,
            "group": self.group,
            "score": self.score,
            "extensions": self.extensions,
        }
    
    def __str__(self) -> str:
        """Human-readable string representation."""
        confidence = "高" if self.score > 0.9 else ("中" if self.score > 0.7 else "低")
        return f"{self.path}: {self.description} ({confidence}置信度, {self.score:.2%})"


@dataclass
class DetectionResult:
    """Result of file type detection operation."""
    files: List[FileInfo] = field(default_factory=list)
    total_count: int = 0
    success_count: int = 0
    failed_count: int = 0
    errors: List[Dict[str, str]] = field(default_factory=list)
    
    def get_by_label(self, label: str) -> List[FileInfo]:
        """Get files by specific label."""
        return [f for f in self.files if f.label == label]
    
    def get_by_group(self, group: str) -> List[FileInfo]:
        """Get files by file group (code, document, image, etc.)."""
        return [f for f in self.files if f.group == group]
    
    def get_by_extension(self, ext: str) -> List[FileInfo]:
        """Get files by extension."""
        ext = ext if ext.startswith(".") else f".{ext}"
        return [f for f in self.files if ext in f.extensions]
    
    def summary(self) -> Dict[str, int]:
        """Get summary statistics."""
        summary_dict = {}
        for f in self.files:
            summary_dict[f.label] = summary_dict.get(f.label, 0) + 1
        return summary_dict
    
    def to_json(self, indent: int = 2) -> str:
        """Export to JSON string."""
        return json.dumps({
            "total_count": self.total_count,
            "success_count": self.success_count,
            "failed_count": self.failed_count,
            "files": [f.to_dict() for f in self.files],
            "errors": self.errors,
        }, indent=indent, ensure_ascii=False)


class MagikaSDK:
    """
    Enhanced Magika SDK for AI-powered file type detection.
    
    This class provides a simplified and powerful API for detecting file types
    using Google's Magika AI model.
    
    Features:
        - Simple one-line detection for single files
        - Batch processing for directories
        - Configurable detection modes
        - Rich metadata in results
        - Support for bytes, streams, and file paths
    
    Example:
        >>> sdk = MagikaSDK()
        >>> result = sdk.detect_file("document.pdf")
        >>> print(result.label, result.description)
        
        >>> results = sdk.scan_directory("./uploads")
        >>> for file_info in results.files:
        ...     print(f"{file_info.path}: {file_info.label}")
    """
    
    # Label descriptions in Chinese
    LABEL_DESCRIPTIONS_ZH: Dict[str, str] = {
        "python": "Python源代码",
        "javascript": "JavaScript代码",
        "typescript": "TypeScript代码",
        "java": "Java源代码",
        "c": "C源代码",
        "cpp": "C++源代码",
        "csharp": "C#源代码",
        "go": "Go源代码",
        "rust": "Rust源代码",
        "ruby": "Ruby代码",
        "php": "PHP代码",
        "swift": "Swift代码",
        "kotlin": "Kotlin代码",
        "html": "HTML文档",
        "css": "CSS样式表",
        "json": "JSON数据文件",
        "xml": "XML文档",
        "yaml": "YAML配置文件",
        "toml": "TOML配置文件",
        "markdown": "Markdown文档",
        "text": "纯文本文件",
        "pdf": "PDF文档",
        "zip": "ZIP压缩文件",
        "tar": "TAR归档文件",
        "gzip": "GZIP压缩文件",
        "png": "PNG图片",
        "jpg": "JPEG图片",
        "gif": "GIF图片",
        "bmp": "BMP图片",
        "mp3": "MP3音频",
        "mp4": "MP4视频",
        "exe": "Windows可执行文件",
        "dll": "动态链接库",
        "elf": "Linux可执行文件",
        "macho": "macOS可执行文件",
    }
    
    def __init__(
        self,
        mode: DetectionMode = DetectionMode.BEST_GUESS,
        output_labels: str = "en",
        enable_logs: bool = False,
    ):
        """
        Initialize the Magika SDK.
        
        Args:
            mode: Detection mode (high/medium/best/all confidence)
            output_labels: Output language for labels ("en" or "zh")
            enable_logs: Enable debug logs
        """
        if not MAGIKA_AVAILABLE:
            raise ImportError(
                "magika package is not installed. "
                "Please install it with: pip install magika"
            )
        
        self._mode = mode
        self._output_labels = output_labels
        self._magika = MagikaCore()
        
        # Model configuration
        self._score_threshold = self._get_score_threshold(mode)
    
    def _get_score_threshold(self, mode: DetectionMode) -> float:
        """Get score threshold based on detection mode."""
        thresholds = {
            DetectionMode.HIGH_CONFIDENCE: 0.9,
            DetectionMode.MEDIUM_CONFIDENCE: 0.7,
            DetectionMode.BEST_GUESS: 0.0,
            DetectionMode.ALL: 0.0,
        }
        return thresholds.get(mode, 0.0)
    
    def _convert_result(self, magika_result: MagikaResult, path: str) -> FileInfo:
        """Convert Magika result to FileInfo."""
        output = magika_result.output
        
        return FileInfo(
            path=path,
            label=output.label,
            description=output.description,
            mime_type=output.more_info.mime_type if hasattr(output, 'more_info') else "",
            is_text=output.is_text,
            group=output.group,
            score=magika_result.score,
            extensions=list(output.more_info.extensions) if hasattr(output, 'more_info') else [],
        )
    
    def detect_bytes(self, data: bytes, path: str = "unknown") -> FileInfo:
        """
        Detect file type from bytes data.
        
        Args:
            data: Raw bytes data
            path: Optional path for reference
            
        Returns:
            FileInfo with detection results
        """
        result = self._magika.identify_bytes(data)
        return self._convert_result(result, path)
    
    def detect_file(self, file_path: Union[str, Path]) -> FileInfo:
        """
        Detect file type from a single file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            FileInfo with detection results
        """
        path = str(file_path)
        
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
        
        if not os.path.isfile(path):
            raise ValueError(f"Path is not a file: {path}")
        
        result = self._magika.identify_path(path)
        return self._convert_result(result, path)
    
    def scan_directory(
        self,
        directory: Union[str, Path],
        recursive: bool = True,
        extensions_filter: Optional[List[str]] = None,
        exclude_patterns: Optional[List[str]] = None,
    ) -> DetectionResult:
        """
        Scan a directory for file type detection.
        
        Args:
            directory: Directory path to scan
            recursive: Scan subdirectories recursively
            extensions_filter: Only scan files with these extensions
            exclude_patterns: Skip files matching these patterns
            
        Returns:
            DetectionResult with all detected files
        """
        dir_path = Path(directory)
        
        if not dir_path.exists():
            raise FileNotFoundError(f"Directory not found: {directory}")
        
        if not dir_path.is_dir():
            raise ValueError(f"Path is not a directory: {directory}")
        
        result = DetectionResult()
        
        # Collect files
        if recursive:
            files = list(dir_path.rglob("*"))
        else:
            files = list(dir_path.glob("*"))
        
        files = [f for f in files if f.is_file()]
        
        # Apply filters
        if extensions_filter:
            extensions_filter = [ext.lower() if ext.startswith(".") else f".{ext.lower()}" for ext in extensions_filter]
            files = [f for f in files if f.suffix.lower() in extensions_filter]
        
        if exclude_patterns:
            for pattern in exclude_patterns:
                files = [f for f in files if not f.match(pattern)]
        
        result.total_count = len(files)
        
        # Process files
        for file_path in files:
            try:
                file_info = self.detect_file(file_path)
                
                # Apply score threshold
                if file_info.score >= self._score_threshold:
                    result.files.append(file_info)
                    result.success_count += 1
                    
            except Exception as e:
                result.failed_count += 1
                result.errors.append({
                    "path": str(file_path),
                    "error": str(e),
                })
        
        return result
    
    def get_supported_types(self) -> List[Dict[str, Any]]:
        """
        Get list of all supported file types.
        
        Returns:
            List of supported file types with metadata
        """
        return [
            {"label": k, "description": v}
            for k, v in self.LABEL_DESCRIPTIONS_ZH.items()
        ]
    
    def get_file_group_description(self, group: str) -> str:
        """Get Chinese description for file group."""
        groups = {
            "code": "代码文件",
            "document": "文档文件",
            "image": "图片文件",
            "audio": "音频文件",
            "video": "视频文件",
            "archive": "压缩归档",
            "executable": "可执行文件",
            "data": "数据文件",
        }
        return groups.get(group, group)


# Global instance for convenience
@lru_cache(maxsize=1)
def get_instance(mode: DetectionMode = DetectionMode.BEST_GUESS) -> MagikaSDK:
    """
    Get a cached global instance of MagikaSDK.
    
    Args:
        mode: Detection mode
        
    Returns:
        MagikaSDK instance
    """
    return MagikaSDK(mode=mode)
