# 🎯 Magika SDK Python

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/AI-File%20Detection-purple.svg" alt="AI Detection">
  <img src="https://img.shields.io/badge/Status-Stable-brightgreen.svg" alt="Status">
</p>

<p align="center">
  <a href="README.md">简体中文</a> | <a href="README.zh-TW.md">繁體中文</a> | <strong>English</strong> | <a href="README.ja.md">日本語</a>
</p>

---

## 🎉 Project Introduction

**Magika SDK Python** is an enhanced Python SDK for AI-powered file type detection, based on Google's Magika AI engine. It provides out-of-the-box deep learning file identification capabilities.

### 🔥 Core Value

| Feature | Description |
|---------|-------------|
| 🤖 **AI Powered** | Deep learning model based, 99%+ accuracy |
| ⚡ **Lightning Fast** | ~5ms inference per file, regardless of file size |
| 📦 **Feature Rich** | Supports 200+ file type detection |
| 🔒 **Security Scanning** | Built-in enterprise security threat detection |
| 🌐 **Async Processing** | Large-scale directory async concurrent scanning |
| 📖 **Chinese Documentation** | Full Chinese docs, developer friendly |

### 💡 Inspiration

This project is inspired by [google/magika](https://github.com/google/magika), with deep enhancements and additional features to provide simpler and more powerful file type detection for Python developers.

### 🚀 Differentiation Highlights

1. **Simpler Python API** - One line of code for file type detection
2. **Async Batch Processing** - High-concurrency scanning with progress bar
3. **Enterprise Security** - Built-in threat detection, misnamed file identification, security reports
4. **Chinese Localization** - Full Chinese documentation and error messages
5. **Enhanced Filtering** - Filter results by type, group, extension

---

## ✨ Core Features

### 📋 Feature List

| Feature | Description | Status |
|---------|-------------|--------|
| 📄 Single File Detection | bytes / stream / path input methods | ✅ |
| 📁 Batch Directory Scan | Recursive scan, extension filtering | ✅ |
| ⚡ Async Concurrent Processing | Large-scale parallel scanning with progress | ✅ |
| 🔍 Security Threat Detection | Identify malware, executables, scripts | ✅ |
| 🚨 Misnamed File Detection | Detect extension/content mismatch | ✅ |
| 📊 Security Report Generation | Generate structured security audit reports | ✅ |
| 🎯 Multiple Detection Modes | High/Medium/Best confidence modes | ✅ |
| 📤 JSON Export | Export results as JSON | ✅ |

### 🛠️ Tech Stack

```
┌─────────────────────────────────────────────┐
│              Magika SDK Python              │
├─────────────────────────────────────────────┤
│  Magika Core (Google)  │  Python 3.8+       │
│  aiofiles             │  tqdm              │
│  asyncio              │  concurrent.futures │
├─────────────────────────────────────────────┤
│  Supported: Windows / macOS / Linux          │
└─────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### 📥 Installation

```bash
# Install from PyPI (recommended)
pip install magika-sdk-python

# Or install dev version
pip install git+https://github.com/gitstq/magika-sdk-python.git

# Install dependencies
pip install magika aiofiles tqdm
```

### 📋 Requirements

| Environment | Requirement |
|-------------|-------------|
| Python | 3.8+ |
| OS | Windows / macOS / Linux |
| Memory | 4GB+ recommended |
| Disk | ~100MB (including Magika model) |

### 🏃 Quick Usage

#### 1️⃣ Basic Detection

```python
from magika_sdk import MagikaSDK, DetectionMode

# Initialize SDK
sdk = MagikaSDK(mode=DetectionMode.BEST_GUESS)

# Detect single file
result = sdk.detect_file("document.pdf")
print(f"File type: {result.label}")          # pdf
print(f"Description: {result.description}") # PDF document
print(f"Confidence: {result.score:.2%}")     # 99.50%

# Detect from bytes
bytes_result = sdk.detect_bytes(b'print("Hello")')
print(f"Type: {bytes_result.label}")        # python
```

#### 2️⃣ Batch Directory Scan

```python
from magika_sdk import MagikaSDK

sdk = MagikaSDK()

# Scan directory
result = sdk.scan_directory("./my_folder")

# Print statistics
print(f"Total files: {result.total_count}")
print(f"Successful: {result.success_count}")

# Filter by type
python_files = result.get_by_label("python")
json_files = result.get_by_group("data")

# Print summary
for label, count in result.summary().items():
    print(f"{label}: {count}")
```

#### 3️⃣ Async Batch Processing

```python
import asyncio
from magika_sdk import AsyncMagikaScanner

async def scan():
    scanner = AsyncMagikaScanner(max_workers=20)
    
    result = await scanner.scan_directory_async(
        "./large_folder",
        recursive=True,
        progress_callback=lambda done, total: print(f"\rProgress: {done}/{total}", end="")
    )
    
    print(f"\nScan complete! {result.total_count} files processed")
    scanner.close()

asyncio.run(scan())
```

#### 4️⃣ Security Scanning

```python
from magika_sdk import SecurityScanner

scanner = SecurityScanner()

# Scan directory for threats
report = scanner.scan_directory("./uploads")

# Generate security report
print(scanner.generate_summary(report))

# Get critical threats
critical = report.get_critical_findings()
high_risk = report.get_high_findings()
misnamed = report.get_misnamed_files()

# Export JSON report
import json
print(json.dumps(report.export_report(), indent=2, ensure_ascii=False))
```

---

## 📖 Detailed Usage Guide

### Detection Modes

```python
from magika_sdk import DetectionMode

# High confidence mode - only return high confidence results
sdk = MagikaSDK(mode=DetectionMode.HIGH_CONFIDENCE)

# Medium confidence mode - include medium confidence results
sdk = MagikaSDK(mode=DetectionMode.MEDIUM_CONFIDENCE)

# Best guess mode - always return best guess
sdk = MagikaSDK(mode=DetectionMode.BEST_GUESS)
```

### File Type Filters

```python
sdk = MagikaSDK()

# Scan only specific extensions
result = sdk.scan_directory(
    "./folder",
    extensions_filter=[".py", ".js", ".json"]
)

# Exclude specific patterns
result = sdk.scan_directory(
    "./folder",
    exclude_patterns=["*.test.*", "node_modules/*"]
)
```

### Async Multi-Directory Scan

```python
from magika_sdk import AsyncMagikaScanner

async def scan_multiple():
    scanner = AsyncMagikaScanner(max_workers=10)
    
    # Scan multiple directories simultaneously
    result = await scanner.scan_multiple_directories([
        "./src",
        "./lib",
        "./tests"
    ])
    
    print(f"Scanned {result.total_count} files in total")
    scanner.close()

asyncio.run(scan_multiple())
```

### Security Scanner Configuration

```python
from magika_sdk import SecurityScanner

# Enable misnamed file detection
scanner = SecurityScanner(check_misnamed=True)

# Strict mode (stricter threat detection)
scanner = SecurityScanner(strict_mode=True)
```

---

## 📊 Example Output

### File Detection Result

```
File path: ./samples/document.pdf
File type: pdf
Description: PDF document
MIME type: application/pdf
Confidence: 99.85%
Is text: False
File group: document
```

### Security Scan Report

```
============================================================
📋 Security Scan Report Summary
============================================================
Scan time: 2024-01-15 14:30:00
Total files scanned: 150

🔢 Threat Level Distribution:
  ✅ Safe: 120
  ⚠️  Low: 15
  🔶 Medium: 10
  🔴 High: 5
  🚫 Critical: 0

🚨 High Risk Threats (Immediate Action Required):
  • uploads/backup.bat
    Reason: Batch script file detected
    Recommendation: Check script content for malicious code

🔍 Misnamed Files (Extension/Content Mismatch):
  • uploads/image.jpg.exe
    Extension suggests image, but content is executable
============================================================
```

---

## 💡 Design Philosophy & Roadmap

### Design Principles

1. **Simplicity First** - One line of code for complex features
2. **Type Safety** - Complete type annotations and type checking
3. **Error Handling** - Robust exception handling and friendly error messages
4. **Performance** - Async processing and concurrency control

### Tech Choices

| Component | Reason |
|-----------|--------|
| Magika Core | Google's production, mature and stable |
| asyncio | Python native async support, no extra deps |
| tqdm | Mature progress bar library, great UX |
| aiofiles | Async file I/O for better large file handling |

### Roadmap

- [ ] v1.1.0 - Add file content hashing (MD5/SHA256)
- [ ] v1.2.0 - Support custom model loading
- [ ] v1.3.0 - Add Web service interface (FastAPI)
- [ ] v2.0.0 - CLI tool redesign with better UX

---

## 📦 Packaging & Deployment

### Build Distribution

```bash
# Clone repository
git clone https://github.com/gitstq/magika-sdk-python.git
cd magika-sdk-python

# Install build dependencies
pip install build

# Build wheel and tarball
python -m build

# Upload to PyPI
twine upload dist/*
```

### One-Click Build Script

```bash
# Linux/macOS
./build.sh

# Windows
./build.bat
```

### Publish to GitHub Release

```bash
# Create tag
git tag -a v1.0.0 -m "Release v1.0.0"

# Push tag
git push origin v1.0.0
```

---

## 🤝 Contributing

Issues and Pull Requests are welcome!

### Commit Convention

```
feat: New feature
fix: Bug fix
docs: Documentation update
refactor: Code refactoring
test: Test cases
chore: Build/tool changes
```

### Development Workflow

1. Fork this repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Create Pull Request

---

## 📄 License

This project is open source under [MIT License](LICENSE).

---

## 🙏 Acknowledgments

- [Google Magika](https://github.com/google/magika) - AI file type detection engine
- [aiofiles](https://github.com/Tinche/aiofiles) - Async file I/O
- [tqdm](https://github.com/tqdm/tqdm) - Progress bar component

---

<p align="center">
  <strong>If you find this project helpful, please give it a ⭐ Star!</strong>
</p>
