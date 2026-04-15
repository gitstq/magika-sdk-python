"""
Security Scanner Module
=======================

Enterprise security scenario detection strategies for file type analysis.
Provides threat assessment, malware detection hints, and security audit tools.

This module helps security teams:
- Identify potentially dangerous file types
- Detect disguised/misnamed files
- Audit suspicious file patterns
- Generate security reports

Author: gitstq
License: MIT
"""

import os
from pathlib import Path
from typing import Dict, List, Optional, Set, Union, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

from .core import MagikaSDK, FileInfo, DetectionResult, DetectionMode


class ThreatLevel(Enum):
    """Security threat level classification."""
    SAFE = "safe"           # No threat detected
    LOW = "low"             # Low risk, may need attention
    MEDIUM = "medium"       # Medium risk, review recommended
    HIGH = "high"           # High risk, immediate attention required
    CRITICAL = "critical"   # Critical threat, block immediately


class ThreatCategory(Enum):
    """Categories of security threats."""
    EXECUTABLE = "executable"           # Executable files
    SCRIPT = "script"                     # Script files that can run
    ARCHIVE_SUSPICIOUS = "archive_suspicious"  # Archives that may contain threats
    DOCUMENT_MACRO = "document_macro"     # Documents with potential macros
    OBFUSCATED = "obfuscated"             # Obfuscated/encoded content
    MISNAMED = "misnamed"                # File extension mismatch
    COMPILABLE = "compilable"             # Source code files
    CONFIG_BACKUP = "config_backup"       # Sensitive config files


@dataclass
class SecurityFinding:
    """A single security finding from scanning."""
    file_path: str
    threat_level: ThreatLevel
    category: ThreatCategory
    description: str
    recommendation: str
    detected_label: str
    detected_mime: str
    is_misnamed: bool = False
    details: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for reporting."""
        return {
            "file_path": self.file_path,
            "threat_level": self.threat_level.value,
            "category": self.category.value,
            "description": self.description,
            "recommendation": self.recommendation,
            "detected_label": self.detected_label,
            "detected_mime": self.detected_mime,
            "is_misnamed": self.is_misnamed,
            "details": self.details,
        }


@dataclass
class SecurityReport:
    """Comprehensive security audit report."""
    scan_time: datetime
    total_files: int
    findings: List[SecurityFinding] = field(default_factory=list)
    summary: Dict[str, int] = field(default_factory=dict)
    threat_distribution: Dict[str, int] = field(default_factory=dict)
    
    def get_critical_findings(self) -> List[SecurityFinding]:
        """Get all critical threat findings."""
        return [f for f in self.findings if f.threat_level == ThreatLevel.CRITICAL]
    
    def get_high_findings(self) -> List[SecurityFinding]:
        """Get all high threat findings."""
        return [f for f in self.findings if f.threat_level == ThreatLevel.HIGH]
    
    def get_misnamed_files(self) -> List[SecurityFinding]:
        """Get all misnamed/disguised files."""
        return [f for f in self.findings if f.is_misnamed]
    
    def export_report(self) -> Dict:
        """Export complete report as dictionary."""
        return {
            "scan_time": self.scan_time.isoformat(),
            "total_files": self.total_files,
            "summary": self.summary,
            "threat_distribution": self.threat_distribution,
            "findings": [f.to_dict() for f in self.findings],
            "critical_count": len(self.get_critical_findings()),
            "high_count": len(self.get_high_findings()),
            "misnamed_count": len(self.get_misnamed_files()),
        }


class SecurityScanner:
    """
    Enterprise security scanner for file type analysis.
    
    Provides comprehensive threat detection with:
    - Executable and script file identification
    - Misnamed file detection (extension vs content mismatch)
    - Suspicious archive analysis
    - Macro-enabled document detection
    - Security audit report generation
    
    Example:
        >>> scanner = SecurityScanner()
        >>> report = scanner.scan_directory("./uploads")
        >>> print(f"Found {len(report.get_critical_findings())} critical threats")
    """
    
    # Executable file types (high threat if from untrusted source)
    DANGEROUS_EXECUTABLES: Set[str] = {
        "exe", "dll", "sys", "msi", "bat", "cmd", "ps1", "vbs", "js", "jar",
        "app", "dmg", "pkg", "deb", "rpm", "apk", "xap", "ipa",
    }
    
    # Script file types (can execute arbitrary code)
    DANGEROUS_SCRIPTS: Set[str] = {
        "sh", "bash", "zsh", "py", "rb", "pl", "php", "lua", "perl",
        "ps1", "bat", "cmd", "vbs", "js", "ts", "sql",
    }
    
    # Source code that can be compiled to executables
    COMPILABLE_SOURCES: Set[str] = {
        "c", "cpp", "cxx", "h", "hpp", "java", "cs", "go", "rs", "swift",
        "kt", "scala", "clj", "f", "for", "asm", "s",
    }
    
    # Archives that commonly contain threats
    SUSPICIOUS_ARCHIVES: Set[str] = {
        "zip", "rar", "7z", "tar", "gz", "bz2", "xz", "iso",
    }
    
    # Document types that may contain macros
    MACRO_DOCUMENTS: Set[str] = {
        "doc", "docm", "xls", "xlsm", "ppt", "pptm", "odt", "ods", "odp",
    }
    
    # Potentially obfuscated/encoded files
    OBFUSCATED_TYPES: Set[str] = {
        "bin", "dat", "dump", "blob", "raw",
    }
    
    # File extensions to Magika labels mapping for misnamed detection
    EXTENSION_TO_LABEL: Dict[str, Set[str]] = {
        "exe": {"exe", "elf", "macho"},
        "dll": {"dll", "so", "dylib"},
        "pdf": {"pdf"},
        "doc": {"doc", "docx", "odt"},
        "jpg": {"jpg", "jpeg", "png", "gif"},
        "png": {"png", "jpg", "jpeg", "gif"},
        "zip": {"zip", "gzip", "tar", "archive"},
    }
    
    def __init__(
        self,
        sdk: Optional[MagikaSDK] = None,
        check_misnamed: bool = True,
        strict_mode: bool = False,
    ):
        """
        Initialize the security scanner.
        
        Args:
            sdk: Optional MagikaSDK instance (creates new if not provided)
            check_misnamed: Enable extension/content mismatch detection
            strict_mode: Use stricter threat detection thresholds
        """
        self._sdk = sdk or MagikaSDK()
        self._check_misnamed = check_misnamed
        self._strict_mode = strict_mode
    
    def _get_threat_level(
        self,
        file_info: FileInfo,
        file_ext: str,
    ) -> Tuple[ThreatLevel, ThreatCategory, str, str]:
        """
        Determine threat level for a file.
        
        Returns:
            Tuple of (ThreatLevel, ThreatCategory, description, recommendation)
        """
        label = file_info.label.lower()
        ext = file_ext.lower().lstrip(".")
        
        # Check for misnamed files (high priority)
        if self._check_misnamed:
            expected_labels = self.EXTENSION_TO_LABEL.get(ext, set())
            if expected_labels and label not in expected_labels:
                if label in self.DANGEROUS_EXECUTABLES:
                    return (
                        ThreatLevel.CRITICAL,
                        ThreatCategory.MISNAMED,
                        f"文件扩展名为 {ext} 但实际内容为 {file_info.description}，可能是伪装的恶意文件",
                        f"立即检查此文件来源，禁止从 {ext} 扩展名对应的正常位置执行",
                    )
                elif label in self.DANGEROUS_SCRIPTS:
                    return (
                        ThreatLevel.HIGH,
                        ThreatCategory.MISNAMED,
                        f"文件扩展名为 {ext} 但实际为 {file_info.description}",
                        "检查文件来源和创建者，确认是否为伪装的可执行文件",
                    )
        
        # Check for dangerous executables
        if label in self.DANGEROUS_EXECUTABLES:
            threat = ThreatLevel.HIGH if self._strict_mode else ThreatLevel.MEDIUM
            return (
                threat,
                ThreatCategory.EXECUTABLE,
                f"发现可执行文件类型: {file_info.description}",
                "仅从可信来源执行，建议在沙箱环境中测试",
            )
        
        # Check for dangerous scripts
        if label in self.DANGEROUS_SCRIPTS:
            return (
                ThreatLevel.MEDIUM,
                ThreatCategory.SCRIPT,
                f"发现脚本文件: {file_info.description}",
                "检查脚本内容，确认无恶意代码后再执行",
            )
        
        # Check for compilable sources
        if label in self.COMPILABLE_SOURCES:
            return (
                ThreatLevel.LOW,
                ThreatCategory.COMPILABLE,
                f"发现可编译源代码: {file_info.description}",
                "源代码文件通常风险较低，但可用于生成恶意程序",
            )
        
        # Check for suspicious archives
        if label in self.SUSPICIOUS_ARCHIVES:
            return (
                ThreatLevel.LOW,
                ThreatCategory.ARCHIVE_SUSPICIOUS,
                f"发现压缩归档: {file_info.description}",
                "解压前使用杀毒软件扫描，警惕嵌套压缩",
            )
        
        # Check for macro documents
        if label in self.MACRO_DOCUMENTS:
            return (
                ThreatLevel.MEDIUM,
                ThreatCategory.DOCUMENT_MACRO,
                f"发现可能含宏的文档: {file_info.description}",
                "禁用宏功能，仅在确认安全后启用",
            )
        
        # Check for obfuscated content
        if label in self.OBFUSCATED_TYPES:
            return (
                ThreatLevel.MEDIUM,
                ThreatCategory.OBFUSCATED,
                f"发现混淆/二进制文件: {file_info.description}",
                "分析文件内容，确认是否为正常二进制文件",
            )
        
        return (
            ThreatLevel.SAFE,
            ThreatCategory.EXECUTABLE,  # Default category
            f"文件类型正常: {file_info.description}",
            "无特殊安全建议",
        )
    
    def scan_file(self, file_path: Union[str, Path]) -> Optional[SecurityFinding]:
        """
        Scan a single file for security threats.
        
        Args:
            file_path: Path to the file
            
        Returns:
            SecurityFinding if threats detected, None otherwise
        """
        try:
            file_info = self._sdk.detect_file(file_path)
            path_str = str(file_path)
            ext = Path(file_path).suffix
            
            threat_level, category, description, recommendation = self._get_threat_level(
                file_info, ext
            )
            
            # Skip safe files
            if threat_level == ThreatLevel.SAFE:
                return None
            
            return SecurityFinding(
                file_path=path_str,
                threat_level=threat_level,
                category=category,
                description=description,
                recommendation=recommendation,
                detected_label=file_info.label,
                detected_mime=file_info.mime_type,
                is_misnamed=(
                    self._check_misnamed and
                    ext.lstrip(".").lower() in self.EXTENSION_TO_LABEL and
                    file_info.label not in self.EXTENSION_TO_LABEL.get(ext.lstrip(".").lower(), set())
                ),
                details={
                    "score": file_info.score,
                    "is_text": file_info.is_text,
                    "group": file_info.group,
                },
            )
            
        except Exception as e:
            return SecurityFinding(
                file_path=str(file_path),
                threat_level=ThreatLevel.MEDIUM,
                category=ThreatCategory.OBFUSCATED,
                description=f"扫描失败: {str(e)}",
                recommendation="手动检查此文件",
                detected_label="unknown",
                detected_mime="unknown",
            )
    
    def scan_directory(
        self,
        directory: Union[str, Path],
        recursive: bool = True,
        extensions_filter: Optional[List[str]] = None,
    ) -> SecurityReport:
        """
        Scan a directory for security threats.
        
        Args:
            directory: Directory to scan
            recursive: Scan subdirectories
            extensions_filter: Only scan files with these extensions
            
        Returns:
            Comprehensive SecurityReport
        """
        # Get file detections
        result = self._sdk.scan_directory(
            directory,
            recursive=recursive,
            extensions_filter=extensions_filter,
        )
        
        findings = []
        threat_counts: Dict[str, int] = {
            "safe": 0,
            "low": 0,
            "medium": 0,
            "high": 0,
            "critical": 0,
        }
        category_counts: Dict[str, int] = {}
        
        for file_info in result.files:
            path = Path(file_info.path)
            ext = path.suffix
            
            threat_level, category, description, recommendation = self._get_threat_level(
                file_info, ext
            )
            
            threat_counts[threat_level.value] += 1
            
            if threat_level != ThreatLevel.SAFE:
                category_counts[category.value] = category_counts.get(category.value, 0) + 1
                
                is_misnamed = (
                    self._check_misnamed and
                    ext.lstrip(".").lower() in self.EXTENSION_TO_LABEL and
                    file_info.label not in self.EXTENSION_TO_LABEL.get(ext.lstrip(".").lower(), set())
                )
                
                findings.append(SecurityFinding(
                    file_path=str(file_info.path),
                    threat_level=threat_level,
                    category=category,
                    description=description,
                    recommendation=recommendation,
                    detected_label=file_info.label,
                    detected_mime=file_info.mime_type,
                    is_misnamed=is_misnamed,
                    details={
                        "score": file_info.score,
                        "is_text": file_info.is_text,
                        "group": file_info.group,
                    },
                ))
        
        # Sort findings by threat level
        findings.sort(key=lambda f: [
            ThreatLevel.CRITICAL,
            ThreatLevel.HIGH,
            ThreatLevel.MEDIUM,
            ThreatLevel.LOW,
            ThreatLevel.SAFE,
        ].index(f.threat_level))
        
        return SecurityReport(
            scan_time=datetime.now(),
            total_files=result.total_count,
            findings=findings,
            summary={
                "total_scanned": result.total_count,
                "threats_found": len(findings),
                "scan_success_rate": f"{(result.success_count/result.total_count*100):.1f}%" if result.total_count > 0 else "N/A",
            },
            threat_distribution=threat_counts,
        )
    
    def generate_summary(self, report: SecurityReport) -> str:
        """
        Generate a human-readable security summary.
        
        Args:
            report: SecurityReport to summarize
            
        Returns:
            Formatted summary string
        """
        lines = [
            "=" * 60,
            "📋 安全扫描报告摘要",
            "=" * 60,
            f"扫描时间: {report.scan_time.strftime('%Y-%m-%d %H:%M:%S')}",
            f"扫描文件总数: {report.total_files}",
            "",
            "🔢 威胁等级分布:",
            f"  ✅ 安全 (Safe): {report.threat_distribution.get('safe', 0)}",
            f"  ⚠️  低危 (Low): {report.threat_distribution.get('low', 0)}",
            f"  🔶 中危 (Medium): {report.threat_distribution.get('medium', 0)}",
            f"  🔴 高危 (High): {report.threat_distribution.get('high', 0)}",
            f"  🚫 严重 (Critical): {report.threat_distribution.get('critical', 0)}",
            "",
            f"📊 发现威胁总数: {len(report.findings)}",
            "",
        ]
        
        if report.get_critical_findings():
            lines.extend([
                "🚨 严重威胁 (需立即处理):",
            ])
            for f in report.get_critical_findings():
                lines.append(f"  • {f.file_path}")
                lines.append(f"    原因: {f.description}")
                lines.append(f"    建议: {f.recommendation}")
            lines.append("")
        
        if report.get_misnamed_files():
            lines.extend([
                "🔍 伪装文件 (扩展名与内容不符):",
            ])
            for f in report.get_misnamed_files():
                lines.append(f"  • {f.file_path}")
                lines.append(f"    扩展名检测为某类型，但实际内容为 {f.detected_label}")
            lines.append("")
        
        lines.append("=" * 60)
        
        return "\n".join(lines)
