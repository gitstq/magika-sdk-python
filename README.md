# 🎯 Magika SDK Python

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/AI-File%20Detection-purple.svg" alt="AI Detection">
  <img src="https://img.shields.io/badge/Status-Stable-brightgreen.svg" alt="Status">
</p>

<p align="center">
  <strong>English</strong> | <a href="README.zh-TW.md">繁體中文</a> | <a href="README.en.md">English</a> | <a href="README.ja.md">日本語</a>
</p>

---

## 🎉 项目介绍

**Magika SDK Python** 是一款基于 Google Magika AI 引擎增强的 Python 文件类型检测 SDK，提供开箱即用的深度学习文件识别能力。

### 🔥 核心价值

| 特性 | 描述 |
|------|------|
| 🤖 **AI 驱动** | 基于深度学习模型，99%+ 识别准确率 |
| ⚡ **极速检测** | 单文件 ~5ms 推理速度，与文件大小无关 |
| 📦 **功能丰富** | 支持 200+ 文件类型检测 |
| 🔒 **安全扫描** | 内置企业级安全威胁检测策略 |
| 🌐 **异步处理** | 支持大规模目录异步并发扫描 |
| 📖 **中文文档** | 全中文文档，本土开发者友好 |

### 💡 灵感来源

本项目受 [google/magika](https://github.com/google/magika) 启发，在其基础上进行了深度封装和功能增强，专门为 Python 开发者提供更简洁、更强大的文件类型检测能力。

### 🚀 与原版 Magika 的差异化亮点

1. **更简洁的 Python API** - 一行代码完成文件类型检测
2. **异步批量处理** - 支持大规模目录的高并发扫描，带进度条
3. **企业安全场景** - 内置威胁检测、伪装文件识别、安全报告生成
4. **中文本地化** - 全中文文档和错误提示
5. **增强的结果过滤** - 支持按类型、分组、扩展名过滤结果

---

## ✨ 核心特性

### 📋 功能列表

| 功能 | 说明 | 状态 |
|------|------|------|
| 📄 单文件检测 | bytes / stream / path 三种输入方式 | ✅ |
| 📁 批量目录扫描 | 支持递归扫描、扩展名过滤 | ✅ |
| ⚡ 异步并发处理 | 支持大规模并行扫描，带进度条 | ✅ |
| 🔍 安全威胁检测 | 识别恶意文件、可执行文件、脚本 | ✅ |
| 🚨 伪装文件识别 | 检测扩展名与内容不匹配的文件 | ✅ |
| 📊 安全报告生成 | 生成结构化安全审计报告 | ✅ |
| 🎯 多检测模式 | 高/中/最佳置信度模式 | ✅ |
| 📤 JSON 导出 | 支持结果导出为 JSON 格式 | ✅ |

### 🛠️ 技术栈

```
┌─────────────────────────────────────────────┐
│              Magika SDK Python              │
├─────────────────────────────────────────────┤
│  Magika Core (Google)  │  Python 3.8+       │
│  aiofiles             │  tqdm              │
│  asyncio              │  concurrent.futures │
├─────────────────────────────────────────────┤
│  支持平台: Windows / macOS / Linux          │
└─────────────────────────────────────────────┘
```

---

## 🚀 快速开始

### 📥 安装

```bash
# 从 PyPI 安装 (推荐)
pip install magika-sdk-python

# 或安装开发版本
pip install git+https://github.com/gitstq/magika-sdk-python.git

# 安装依赖
pip install magika aiofiles tqdm
```

### 📋 环境要求

| 环境 | 要求 |
|------|------|
| Python | 3.8+ |
| 操作系统 | Windows / macOS / Linux |
| 内存 | 推荐 4GB+ |
| 磁盘 | ~100MB (含 Magika 模型) |

### 🏃 快速使用

#### 1️⃣ 基础检测

```python
from magika_sdk import MagikaSDK, DetectionMode

# 初始化 SDK
sdk = MagikaSDK(mode=DetectionMode.BEST_GUESS)

# 检测单个文件
result = sdk.detect_file("document.pdf")
print(f"文件类型: {result.label}")          # pdf
print(f"描述: {result.description}")       # PDF document
print(f"置信度: {result.score:.2%}")        # 99.50%

# 检测字节数据
bytes_result = sdk.detect_bytes(b'print("Hello")')
print(f"类型: {bytes_result.label}")       # python
```

#### 2️⃣ 批量目录扫描

```python
from magika_sdk import MagikaSDK

sdk = MagikaSDK()

# 扫描目录
result = sdk.scan_directory("./my_folder")

# 打印统计
print(f"总文件数: {result.total_count}")
print(f"成功检测: {result.success_count}")

# 按类型筛选
python_files = result.get_by_label("python")
json_files = result.get_by_group("data")

# 打印摘要
for label, count in result.summary().items():
    print(f"{label}: {count}")
```

#### 3️⃣ 异步批量处理

```python
import asyncio
from magika_sdk import AsyncMagikaScanner

async def scan():
    scanner = AsyncMagikaScanner(max_workers=20)
    
    result = await scanner.scan_directory_async(
        "./large_folder",
        recursive=True,
        progress_callback=lambda done, total: print(f"\r进度: {done}/{total}", end="")
    )
    
    print(f"\n扫描完成! 共 {result.total_count} 个文件")
    scanner.close()

asyncio.run(scan())
```

#### 4️⃣ 安全扫描

```python
from magika_sdk import SecurityScanner

scanner = SecurityScanner()

# 扫描目录查找威胁
report = scanner.scan_directory("./uploads")

# 生成安全报告
print(scanner.generate_summary(report))

# 获取严重威胁
critical = report.get_critical_findings()
high_risk = report.get_high_findings()
misnamed = report.get_misnamed_files()

# 导出 JSON 报告
import json
print(json.dumps(report.export_report(), indent=2, ensure_ascii=False))
```

---

## 📖 详细使用指南

### 检测模式

```python
from magika_sdk import DetectionMode

# 高置信度模式 - 只返回高置信度结果
sdk = MagikaSDK(mode=DetectionMode.HIGH_CONFIDENCE)

# 中置信度模式 - 包含中等置信度结果
sdk = MagikaSDK(mode=DetectionMode.MEDIUM_CONFIDENCE)

# 最佳猜测模式 - 始终返回最佳猜测
sdk = MagikaSDK(mode=DetectionMode.BEST_GUESS)
```

### 文件类型过滤器

```python
sdk = MagikaSDK()

# 只扫描特定扩展名
result = sdk.scan_directory(
    "./folder",
    extensions_filter=[".py", ".js", ".json"]
)

# 排除特定模式
result = sdk.scan_directory(
    "./folder",
    exclude_patterns=["*.test.*", "node_modules/*"]
)
```

### 异步多目录扫描

```python
from magika_sdk import AsyncMagikaScanner

async def scan_multiple():
    scanner = AsyncMagikaScanner(max_workers=10)
    
    # 同时扫描多个目录
    result = await scanner.scan_multiple_directories([
        "./src",
        "./lib",
        "./tests"
    ])
    
    print(f"共扫描 {result.total_count} 个文件")
    scanner.close()

asyncio.run(scan_multiple())
```

### 安全扫描配置

```python
from magika_sdk import SecurityScanner

# 启用伪装文件检测
scanner = SecurityScanner(check_misnamed=True)

# 严格模式 (更严格的威胁检测)
scanner = SecurityScanner(strict_mode=True)
```

---

## 📊 示例输出

### 文件检测结果

```
文件路径: ./samples/document.pdf
文件类型: pdf
描述: PDF document
MIME 类型: application/pdf
置信度: 99.85%
是否为文本: False
文件分组: document
```

### 安全扫描报告

```
============================================================
📋 安全扫描报告摘要
============================================================
扫描时间: 2024-01-15 14:30:00
扫描文件总数: 150

🔢 威胁等级分布:
  ✅ 安全 (Safe): 120
  ⚠️  低危 (Low): 15
  🔶 中危 (Medium): 10
  🔴 高危 (High): 5
  🚫 严重 (Critical): 0

🚨 高危威胁 (需立即处理):
  • uploads/backup.bat
    原因: 发现批处理脚本文件
    建议: 检查脚本内容，确认无恶意代码

🔍 伪装文件 (扩展名与内容不符):
  • uploads/image.jpg.exe
    扩展名检测为图片，但实际内容为可执行文件
============================================================
```

---

## 💡 设计思路与迭代规划

### 设计理念

1. **简洁优先** - 一行代码完成复杂功能
2. **类型安全** - 完整的类型注解和类型检查
3. **错误处理** - 健壮的异常捕获和友好的错误提示
4. **性能优化** - 异步处理和并发控制

### 技术选型

| 组件 | 选型理由 |
|------|----------|
| Magika Core | Google 出品，成熟稳定，准确率高 |
| asyncio | Python 原生异步支持，无需额外依赖 |
| tqdm | 成熟的进度条库，用户体验好 |
| aiofiles | 异步文件 I/O，提升大文件处理效率 |

### 后续迭代计划

- [ ] v1.1.0 - 添加文件内容摘要功能 (支持 MD5/SHA256)
- [ ] v1.2.0 - 支持自定义模型加载
- [ ] v1.3.0 - 添加 Web 服务接口 (FastAPI)
- [ ] v2.0.0 - CLI 工具重构，增强交互体验

---

## 📦 打包与部署

### 构建发布包

```bash
# 克隆仓库
git clone https://github.com/gitstq/magika-sdk-python.git
cd magika-sdk-python

# 安装构建依赖
pip install build

# 构建 wheel 和 tarball
python -m build

# 上传到 PyPI
twine upload dist/*
```

### 一键构建脚本

```bash
# Linux/macOS
./build.sh

# Windows
./build.bat
```

### 发布到 GitHub Release

```bash
# 创建 tag
git tag -a v1.0.0 -m "Release v1.0.0"

# 推送 tag
git push origin v1.0.0
```

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 提交规范

```
feat: 新增功能
fix: 修复问题
docs: 文档更新
refactor: 代码重构
test: 测试用例
chore: 构建/工具变更
```

### 开发流程

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

---

## 📄 开源协议

本项目基于 [MIT License](LICENSE) 开源。

---

## 🙏 致谢

- [Google Magika](https://github.com/google/magika) - AI 文件类型检测引擎
- [aiofiles](https://github.com/Tinche/aiofiles) - 异步文件 I/O
- [tqdm](https://github.com/tqdm/tqdm) - 进度条组件

---

<p align="center">
  <strong>如果你觉得这个项目有帮助，请给个 ⭐ Star！</strong>
</p>
