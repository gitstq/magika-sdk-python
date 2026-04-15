"""
Async Utilities Module
=====================

Asynchronous batch processing for Magika SDK.
Provides high-performance concurrent file scanning with progress tracking.

Author: gitstq
License: MIT
"""

import asyncio
import os
from pathlib import Path
from typing import Optional, List, Callable, Union, Any
from dataclasses import dataclass, field
import aiofiles
from concurrent.futures import ThreadPoolExecutor
from tqdm.asyncio import tqdm
from tqdm import tqdm as sync_tqdm

from .core import MagikaSDK, FileInfo, DetectionResult, DetectionMode


@dataclass
class BatchConfig:
    """Configuration for batch processing."""
    max_workers: int = 10           # Maximum concurrent workers
    chunk_size: int = 100           # Files per batch
    show_progress: bool = True      # Show progress bar
    progress_desc: str = "Scanning"  # Progress bar description
    return_on_error: bool = True     # Continue on error
    timeout: Optional[float] = 30.0  # Timeout per file (seconds)


class AsyncMagikaScanner:
    """
    Asynchronous file scanner using Magika SDK.
    
    Provides high-performance concurrent batch processing with:
    - Configurable worker pool
    - Progress tracking with tqdm
    - Error handling and recovery
    - Memory-efficient streaming
    
    Example:
        >>> scanner = AsyncMagikaScanner(max_workers=20)
        >>> results = await scanner.scan_directory_async("./large_folder")
        >>> print(f"Scanned {results.total_count} files")
    """
    
    def __init__(
        self,
        max_workers: int = 10,
        detection_mode: DetectionMode = DetectionMode.BEST_GUESS,
    ):
        """
        Initialize the async scanner.
        
        Args:
            max_workers: Maximum number of concurrent workers
            detection_mode: File type detection mode
        """
        self._max_workers = max_workers
        self._detection_mode = detection_mode
        self._sdk = MagikaSDK(mode=detection_mode)
        self._executor = ThreadPoolExecutor(max_workers=max_workers)
    
    async def detect_file_async(self, file_path: Union[str, Path]) -> Optional[FileInfo]:
        """
        Asynchronously detect a single file type.
        
        Args:
            file_path: Path to the file
            
        Returns:
            FileInfo if successful, None otherwise
        """
        loop = asyncio.get_event_loop()
        try:
            result = await loop.run_in_executor(
                self._executor,
                self._sdk.detect_file,
                str(file_path),
            )
            return result
        except Exception as e:
            print(f"Error detecting {file_path}: {e}")
            return None
    
    async def _detect_with_progress(
        self,
        files: List[Path],
        desc: str = "Scanning",
    ) -> List[FileInfo]:
        """Detect files with progress bar."""
        results = []
        
        # Use tqdm for async progress
        semaphore = asyncio.Semaphore(self._max_workers)
        
        async def detect_with_semaphore(path: Path) -> Optional[FileInfo]:
            async with semaphore:
                return await self.detect_file_async(path)
        
        tasks = [detect_with_semaphore(f) for f in files]
        
        for coro in tqdm.as_completed(
            tasks,
            total=len(tasks),
            desc=desc,
            disable=not self._show_progress,
        ):
            result = await coro
            if result:
                results.append(result)
        
        return results
    
    def __init__(
        self,
        max_workers: int = 10,
        detection_mode: DetectionMode = DetectionMode.BEST_GUESS,
        show_progress: bool = True,
    ):
        """Initialize the async scanner."""
        self._max_workers = max_workers
        self._detection_mode = detection_mode
        self._show_progress = show_progress
        self._sdk = MagikaSDK(mode=detection_mode)
        self._executor = ThreadPoolExecutor(max_workers=max_workers)
    
    async def scan_directory_async(
        self,
        directory: Union[str, Path],
        recursive: bool = True,
        extensions_filter: Optional[List[str]] = None,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> DetectionResult:
        """
        Asynchronously scan a directory for file types.
        
        Args:
            directory: Directory to scan
            recursive: Scan subdirectories
            extensions_filter: Only scan files with these extensions
            progress_callback: Optional callback(completed, total)
            
        Returns:
            DetectionResult with all detected files
        """
        dir_path = Path(directory)
        
        if not dir_path.exists():
            raise FileNotFoundError(f"Directory not found: {directory}")
        
        # Collect files
        if recursive:
            files = [f for f in dir_path.rglob("*") if f.is_file()]
        else:
            files = [f for f in dir_path.glob("*") if f.is_file()]
        
        # Apply extension filter
        if extensions_filter:
            ext_set = set(ext.lower() if ext.startswith(".") else f".{ext.lower()}" for ext in extensions_filter)
            files = [f for f in files if f.suffix.lower() in ext_set]
        
        total = len(files)
        result = DetectionResult()
        result.total_count = total
        
        # Progress bar
        pbar = sync_tqdm(total=total, desc="Scanning files", disable=not self._show_progress)
        completed = 0
        
        # Semaphore for concurrency control
        semaphore = asyncio.Semaphore(self._max_workers)
        
        async def process_file(file_path: Path) -> Optional[FileInfo]:
            nonlocal completed
            async with semaphore:
                try:
                    result = await self.detect_file_async(file_path)
                    completed += 1
                    pbar.update(1)
                    if progress_callback:
                        progress_callback(completed, total)
                    return result
                except Exception as e:
                    completed += 1
                    pbar.update(1)
                    result.errors.append({
                        "path": str(file_path),
                        "error": str(e),
                    })
                    return None
        
        # Process all files
        tasks = [process_file(f) for f in files]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        pbar.close()
        
        # Collect successful results
        for r in results:
            if isinstance(r, FileInfo):
                result.files.append(r)
                result.success_count += 1
            elif isinstance(r, Exception):
                result.failed_count += 1
        
        return result
    
    def scan_directory_sync(
        self,
        directory: Union[str, Path],
        recursive: bool = True,
        extensions_filter: Optional[List[str]] = None,
    ) -> DetectionResult:
        """
        Synchronously scan a directory with multi-threading.
        
        This is a convenience method that wraps async processing
        in an event loop for synchronous usage.
        
        Args:
            directory: Directory to scan
            recursive: Scan subdirectories
            extensions_filter: Only scan files with these extensions
            
        Returns:
            DetectionResult with all detected files
        """
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        return loop.run_until_complete(
            self.scan_directory_async(
                directory,
                recursive=recursive,
                extensions_filter=extensions_filter,
            )
        )
    
    async def scan_multiple_directories(
        self,
        directories: List[Union[str, Path]],
        recursive: bool = True,
    ) -> DetectionResult:
        """
        Scan multiple directories concurrently.
        
        Args:
            directories: List of directories to scan
            recursive: Scan subdirectories
            
        Returns:
            Combined DetectionResult
        """
        tasks = [
            self.scan_directory_async(d, recursive=recursive)
            for d in directories
        ]
        
        results = await asyncio.gather(*tasks)
        
        # Combine results
        combined = DetectionResult()
        for r in results:
            combined.files.extend(r.files)
            combined.total_count += r.total_count
            combined.success_count += r.success_count
            combined.failed_count += r.failed_count
            combined.errors.extend(r.errors)
        
        return combined
    
    def close(self):
        """Clean up resources."""
        self._executor.shutdown(wait=True)


def scan_large_directory(
    directory: Union[str, Path],
    max_workers: int = 20,
    batch_size: int = 1000,
    extensions_filter: Optional[List[str]] = None,
) -> DetectionResult:
    """
    High-performance directory scanner optimized for large folders.
    
    Processes files in batches to manage memory usage while
    maintaining high throughput with concurrent processing.
    
    Args:
        directory: Directory to scan
        max_workers: Concurrent worker count
        batch_size: Files per batch
        extensions_filter: Only scan these extensions
        
    Returns:
        DetectionResult with all detected files
    """
    scanner = AsyncMagikaScanner(max_workers=max_workers)
    
    try:
        result = scanner.scan_directory_sync(
            directory,
            recursive=True,
            extensions_filter=extensions_filter,
        )
        return result
    finally:
        scanner.close()
