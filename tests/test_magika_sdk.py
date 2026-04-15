"""
Tests Module
============

Unit tests for Magika SDK Python package.

Run with: pytest tests/ -v
"""

import pytest
import os
import tempfile
from pathlib import Path

from magika_sdk import (
    MagikaSDK,
    FileInfo,
    DetectionResult,
    DetectionMode,
    AsyncMagikaScanner,
    SecurityScanner,
    ThreatLevel,
    ThreatCategory,
)


class TestMagikaSDK:
    """Test cases for MagikaSDK core functionality."""
    
    @pytest.fixture
    def sdk(self):
        """Create SDK instance for testing."""
        return MagikaSDK(mode=DetectionMode.BEST_GUESS)
    
    @pytest.fixture
    def temp_file(self):
        """Create a temporary test file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('print("Hello World")')
            temp_path = f.name
        
        yield temp_path
        os.unlink(temp_path)
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory with test files."""
        temp_dir = tempfile.mkdtemp()
        
        # Create test files
        test_files = [
            ('test.py', 'print("Python")'),
            ('test.js', 'console.log("JavaScript")'),
            ('test.json', '{"key": "value"}'),
            ('test.txt', 'Plain text content'),
        ]
        
        for filename, content in test_files:
            filepath = os.path.join(temp_dir, filename)
            with open(filepath, 'w') as f:
                f.write(content)
        
        yield temp_dir
        
        # Cleanup
        for filename, _ in test_files:
            filepath = os.path.join(temp_dir, filename)
            if os.path.exists(filepath):
                os.unlink(filepath)
        os.rmdir(temp_dir)
    
    def test_detect_bytes(self, sdk):
        """Test detection from bytes data."""
        # Python code
        python_code = b'print("Hello World")'
        result = sdk.detect_bytes(python_code)
        
        assert isinstance(result, FileInfo)
        assert result.label == "python"
        assert result.is_text is True
    
    def test_detect_file(self, sdk, temp_file):
        """Test detection from file path."""
        result = sdk.detect_file(temp_file)
        
        assert isinstance(result, FileInfo)
        assert result.path == temp_file
        assert result.label == "python"
        assert result.score > 0
    
    def test_scan_directory(self, sdk, temp_dir):
        """Test directory scanning."""
        result = sdk.scan_directory(temp_dir)
        
        assert isinstance(result, DetectionResult)
        assert result.total_count == 4
        assert result.success_count >= 3  # At least py, js, json should be detected
    
    def test_detection_result_filters(self, sdk, temp_dir):
        """Test DetectionResult filtering methods."""
        result = sdk.scan_directory(temp_dir)
        
        # Test get_by_label
        python_files = result.get_by_label("python")
        assert len(python_files) >= 1
        
        # Test get_by_group
        code_files = result.get_by_group("code")
        assert len(code_files) >= 1
        
        # Test summary
        summary = result.summary()
        assert isinstance(summary, dict)
        assert "python" in summary
    
    def test_invalid_file_path(self, sdk):
        """Test error handling for invalid paths."""
        with pytest.raises(FileNotFoundError):
            sdk.detect_file("/nonexistent/path/to/file.txt")
    
    def test_non_file_path(self, sdk, temp_dir):
        """Test error handling when path is not a file."""
        with pytest.raises(ValueError):
            sdk.detect_file(temp_dir)


class TestAsyncMagikaScanner:
    """Test cases for AsyncMagikaScanner."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory with test files."""
        temp_dir = tempfile.mkdtemp()
        
        for i in range(10):
            filepath = os.path.join(temp_dir, f'test_{i}.txt')
            with open(filepath, 'w') as f:
                f.write(f'Content {i}')
        
        yield temp_dir
        
        # Cleanup
        for i in range(10):
            filepath = os.path.join(temp_dir, f'test_{i}.txt')
            if os.path.exists(filepath):
                os.unlink(filepath)
        os.rmdir(temp_dir)
    
    @pytest.mark.asyncio
    async def test_async_scan(self, temp_dir):
        """Test async directory scanning."""
        scanner = AsyncMagikaScanner(max_workers=5)
        result = await scanner.scan_directory_async(temp_dir)
        
        assert isinstance(result, DetectionResult)
        assert result.total_count == 10
        scanner.close()
    
    def test_sync_scan(self, temp_dir):
        """Test synchronous batch scanning."""
        result = AsyncMagikaScanner.scan_large_directory(
            temp_dir,
            max_workers=5,
        )
        
        assert isinstance(result, DetectionResult)
        assert result.total_count == 10


class TestSecurityScanner:
    """Test cases for SecurityScanner."""
    
    @pytest.fixture
    def security_scanner(self):
        """Create security scanner instance."""
        return SecurityScanner()
    
    @pytest.fixture
    def temp_dir_with_threats(self):
        """Create temp directory with various file types."""
        temp_dir = tempfile.mkdtemp()
        
        # Normal files
        test_files = [
            ('normal.py', 'print("Normal")'),
            ('data.json', '{"data": true}'),
            ('image.png', b'\x89PNG\r\n\x1a\n'),  # PNG header
        ]
        
        # Files that might be detected as threats
        threat_files = [
            ('script.bat', '@echo off'),
            ('executable.exe', b'MZ' + b'\x00' * 100),  # PE header
        ]
        
        for filename, content in test_files + threat_files:
            filepath = os.path.join(temp_dir, filename)
            if isinstance(content, bytes):
                with open(filepath, 'wb') as f:
                    f.write(content)
            else:
                with open(filepath, 'w') as f:
                    f.write(content)
        
        yield temp_dir
        
        # Cleanup
        for files in [test_files, threat_files]:
            for filename, _ in files:
                filepath = os.path.join(temp_dir, filename)
                if os.path.exists(filepath):
                    os.unlink(filepath)
        os.rmdir(temp_dir)
    
    def test_security_scan(self, security_scanner, temp_dir_with_threats):
        """Test security scanning."""
        report = security_scanner.scan_directory(temp_dir_with_threats)
        
        assert isinstance(report, object)
        assert hasattr(report, 'total_files')
        assert hasattr(report, 'findings')
        assert report.total_files == 5
    
    def test_threat_level_classification(self, security_scanner):
        """Test threat level classification."""
        # Test executable file
        temp_file = tempfile.NamedTemporaryFile(suffix='.exe', delete=False)
        temp_file.write(b'MZ' + b'\x00' * 100)
        temp_file.close()
        
        try:
            finding = security_scanner.scan_file(temp_file.name)
            # Should detect something or be None for safe files
            assert finding is None or isinstance(finding.threat_level, ThreatLevel)
        finally:
            os.unlink(temp_file.name)
    
    def test_generate_summary(self, security_scanner, temp_dir_with_threats):
        """Test report summary generation."""
        report = security_scanner.scan_directory(temp_dir_with_threats)
        summary = security_scanner.generate_summary(report)
        
        assert isinstance(summary, str)
        assert "安全扫描报告摘要" in summary or "扫描" in summary


class TestFileInfo:
    """Test cases for FileInfo dataclass."""
    
    def test_file_info_creation(self):
        """Test FileInfo creation."""
        file_info = FileInfo(
            path="/test/path.py",
            label="python",
            description="Python source",
            mime_type="text/x-python",
            is_text=True,
            group="code",
            score=0.99,
            extensions=[".py"],
        )
        
        assert file_info.path == "/test/path.py"
        assert file_info.label == "python"
        assert file_info.score == 0.99
    
    def test_file_info_to_dict(self):
        """Test FileInfo serialization."""
        file_info = FileInfo(
            path="/test/path.py",
            label="python",
            description="Python source",
            mime_type="text/x-python",
            is_text=True,
            group="code",
            score=0.99,
        )
        
        d = file_info.to_dict()
        assert isinstance(d, dict)
        assert d["label"] == "python"
        assert d["score"] == 0.99
    
    def test_file_info_string_representation(self):
        """Test FileInfo string formatting."""
        file_info = FileInfo(
            path="/test/path.py",
            label="python",
            description="Python source",
            mime_type="text/x-python",
            is_text=True,
            group="code",
            score=0.95,
        )
        
        s = str(file_info)
        assert "python" in s.lower()
        assert "Python source" in s


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
