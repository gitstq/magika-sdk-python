# 🎯 Magika SDK Python

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/AI-File%20Detection-purple.svg" alt="AI Detection">
  <img src="https://img.shields.io/badge/Status-Stable-brightgreen.svg" alt="Status">
</p>

<p align="center">
  <strong><a href="README.md">简体中文</a></strong> | 繁體中文 | <a href="README.en.md">English</a> | <a href="README.ja.md">日本語</a>
</p>

---

## 🎉 專案介紹

**Magika SDK Python** 是一款基於 Google Magika AI 引擎增強的 Python 檔案類型檢測 SDK，提供開箱即用的深度學習檔案識別能力。

### 🔥 核心價值

| 特性 | 描述 |
|------|------|
| 🤖 **AI 驅動** | 基於深度學習模型，99%+ 識別準確率 |
| ⚡ **極速檢測** | 單檔案 ~5ms 推理速度，與檔案大小無關 |
| 📦 **功能豐富** | 支援 200+ 檔案類型檢測 |
| 🔒 **安全掃描** | 內建企業級安全威脅檢測策略 |
| 🌐 **非同步處理** | 支援大規模目錄非同步並發掃描 |
| 📖 **中文文件** | 全中文文件，本土開發者友好 |

### 💡 靈感來源

本專案受 [google/magika](https://github.com/google/magika) 啟發，在其基礎上進行了深度封裝和功能增強，專門為 Python 開發者提供更簡潔、更強大的檔案類型檢測能力。

### 🚀 與原版 Magika 的差異化亮點

1. **更簡潔的 Python API** - 一行程式碼完成檔案類型檢測
2. **非同步批量處理** - 支援大規模目錄的高並發掃描，帶進度條
3. **企業安全場景** - 內建威脅檢測、偽裝檔案識別、安全報告生成
4. **中文本地化** - 全中文文件和錯誤提示
5. **增強的結果過濾** - 支援按類型、分組、擴展名過濾結果

---

## ✨ 核心特性

### 📋 功能列表

| 功能 | 說明 | 狀態 |
|------|------|------|
| 📄 單檔案檢測 | bytes / stream / path 三種輸入方式 | ✅ |
| 📁 批量目錄掃描 | 支援遞歸掃描、擴展名過濾 | ✅ |
| ⚡ 非同步並發處理 | 支援大規模平行掃描，帶進度條 | ✅ |
| 🔍 安全威脅檢測 | 識別惡意檔案、可執行檔、腳本 | ✅ |
| 🚨 偽裝檔案識別 | 檢測擴展名與內容不相符的檔案 | ✅ |
| 📊 安全報告生成 | 生成結構化安全審計報告 | ✅ |
| 🎯 多檢測模式 | 高/中/最佳置信度模式 | ✅ |
| 📤 JSON 匯出 | 支援結果匯出為 JSON 格式 | ✅ |

### 🛠️ 技術棧

```
┌─────────────────────────────────────────────┐
│              Magika SDK Python              │
├─────────────────────────────────────────────┤
│  Magika Core (Google)  │  Python 3.8+       │
│  aiofiles             │  tqdm              │
│  asyncio              │  concurrent.futures │
├─────────────────────────────────────────────┤
│  支援平台: Windows / macOS / Linux          │
└─────────────────────────────────────────────┘
```

---

## 🚀 快速開始

### 📥 安裝

```bash
# 從 PyPI 安裝 (推薦)
pip install magika-sdk-python

# 或安裝開發版本
pip install git+https://github.com/gitstq/magika-sdk-python.git

# 安裝依賴
pip install magika aiofiles tqdm
```

### 📋 環境要求

| 環境 | 要求 |
|------|------|
| Python | 3.8+ |
| 作業系統 | Windows / macOS / Linux |
| 記憶體 | 推薦 4GB+ |
| 磁碟 | ~100MB (含 Magika 模型) |

### 🏃 快速使用

#### 1️⃣ 基礎檢測

```python
from magika_sdk import MagikaSDK, DetectionMode

# 初始化 SDK
sdk = MagikaSDK(mode=DetectionMode.BEST_GUESS)

# 檢測單個檔案
result = sdk.detect_file("document.pdf")
print(f"檔案類型: {result.label}")          # pdf
print(f"描述: {result.description}")       # PDF document
print(f"置信度: {result.score:.2%}")        # 99.50%

# 檢測位元組資料
bytes_result = sdk.detect_bytes(b'print("Hello")')
print(f"類型: {bytes_result.label}")       # python
```

#### 2️⃣ 批量目錄掃描

```python
from magika_sdk import MagikaSDK

sdk = MagikaSDK()

# 掃描目錄
result = sdk.scan_directory("./my_folder")

# 列印統計
print(f"總檔案數: {result.total_count}")
print(f"成功檢測: {result.success_count}")

# 按類型篩選
python_files = result.get_by_label("python")
json_files = result.get_by_group("data")

# 列印摘要
for label, count in result.summary().items():
    print(f"{label}: {count}")
```

#### 3️⃣ 非同步批量處理

```python
import asyncio
from magika_sdk import AsyncMagikaScanner

async def scan():
    scanner = AsyncMagikaScanner(max_workers=20)
    
    result = await scanner.scan_directory_async(
        "./large_folder",
        recursive=True,
        progress_callback=lambda done, total: print(f"\r進度: {done}/{total}", end="")
    )
    
    print(f"\n掃描完成! 共 {result.total_count} 個檔案")
    scanner.close()

asyncio.run(scan())
```

#### 4️⃣ 安全掃描

```python
from magika_sdk import SecurityScanner

scanner = SecurityScanner()

# 掃描目錄查找威脅
report = scanner.scan_directory("./uploads")

# 生成安全報告
print(scanner.generate_summary(report))

# 獲取嚴重威脅
critical = report.get_critical_findings()
high_risk = report.get_high_findings()
misnamed = report.get_misnamed_files()

# 匯出 JSON 報告
import json
print(json.dumps(report.export_report(), indent=2, ensure_ascii=False))
```

---

## 📖 詳細使用指南

### 檢測模式

```python
from magika_sdk import DetectionMode

# 高置信度模式 - 只回傳高置信度結果
sdk = MagikaSDK(mode=DetectionMode.HIGH_CONFIDENCE)

# 中置信度模式 - 包含中等置信度結果
sdk = MagikaSDK(mode=DetectionMode.MEDIUM_CONFIDENCE)

# 最佳猜測模式 - 始終回傳最佳猜測
sdk = MagikaSDK(mode=DetectionMode.BEST_GUESS)
```

### 檔案類型過濾器

```python
sdk = MagikaSDK()

# 只掃描特定擴展名
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

### 非同步多目錄掃描

```python
from magika_sdk import AsyncMagikaScanner

async def scan_multiple():
    scanner = AsyncMagikaScanner(max_workers=10)
    
    # 同時掃描多個目錄
    result = await scanner.scan_multiple_directories([
        "./src",
        "./lib",
        "./tests"
    ])
    
    print(f"共掃描 {result.total_count} 個檔案")
    scanner.close()

asyncio.run(scan_multiple())
```

### 安全掃描配置

```python
from magika_sdk import SecurityScanner

# 啟用偽裝檔案檢測
scanner = SecurityScanner(check_misnamed=True)

# 嚴格模式 (更嚴格的威脅檢測)
scanner = SecurityScanner(strict_mode=True)
```

---

## 📊 範例輸出

### 檔案檢測結果

```
檔案路徑: ./samples/document.pdf
檔案類型: pdf
描述: PDF document
MIME 類型: application/pdf
置信度: 99.85%
是否為文字: False
檔案分組: document
```

### 安全掃描報告

```
============================================================
📋 安全掃描報告摘要
============================================================
掃描時間: 2024-01-15 14:30:00
掃描檔案總數: 150

🔢 威脅等級分布:
  ✅ 安全 (Safe): 120
  ⚠️  低危 (Low): 15
  🔶 中危 (Medium): 10
  🔴 高危 (High): 5
  🚫 嚴重 (Critical): 0

🚨 高危威脅 (需立即處理):
  • uploads/backup.bat
    原因: 發現批次處理腳本檔案
    建議: 檢查腳本內容，確認無惡意程式碼

🔍 偽裝檔案 (擴展名與內容不符):
  • uploads/image.jpg.exe
    擴展名檢測為圖片，但實際內容為可執行檔
============================================================
```

---

## 💡 設計思路與迭代規劃

### 設計理念

1. **簡潔優先** - 一行程式碼完成複雜功能
2. **類型安全** - 完整的類型註解和類型檢查
3. **錯誤處理** - 健全的例外捕獲和友善的錯誤提示
4. **效能優化** - 非同步處理和並發控制

### 技術選型

| 元件 | 選型理由 |
|------|----------|
| Magika Core | Google 出品，成熟穩定，準確率高 |
| asyncio | Python 原生非同步支援，無需額外依賴 |
| tqdm | 成熟的進度條庫，使用者體驗好 |
| aiofiles | 非同步檔案 I/O，提升大檔案處理效率 |

### 後續迭代計畫

- [ ] v1.1.0 - 添加檔案內容摘要功能 (支援 MD5/SHA256)
- [ ] v1.2.0 - 支援自訂模型載入
- [ ] v1.3.0 - 添加 Web 服務介面 (FastAPI)
- [ ] v2.0.0 - CLI 工具重構，增強互動體驗

---

## 📦 包裝與部署

### 建構發布包

```bash
# 克隆倉庫
git clone https://github.com/gitstq/magika-sdk-python.git
cd magika-sdk-python

# 安裝建構依賴
pip install build

# 建構 wheel 和 tarball
python -m build

# 上傳到 PyPI
twine upload dist/*
```

### 一鍵建構腳本

```bash
# Linux/macOS
./build.sh

# Windows
./build.bat
```

### 發布到 GitHub Release

```bash
# 建立 tag
git tag -a v1.0.0 -m "Release v1.0.0"

# 推送 tag
git push origin v1.0.0
```

---

## 🤝 貢獻指南

歡迎提交 Issue 和 Pull Request！

### 提交規範

```
feat: 新增功能
fix: 修復問題
docs: 文件更新
refactor: 程式碼重構
test: 測試用例
chore: 建構/工具變更
```

### 開發流程

1. Fork 本倉庫
2. 建立特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送至分支 (`git push origin feature/AmazingFeature`)
5. 建立 Pull Request

---

## 📄 開源協議

本專案基於 [MIT License](LICENSE) 開源。

---

## 🙏 致謝

- [Google Magika](https://github.com/google/magika) - AI 檔案類型檢測引擎
- [aiofiles](https://github.com/Tinche/aiofiles) - 非同步檔案 I/O
- [tqdm](https://github.com/tqdm/tqdm) - 進度條元件

---

<p align="center">
  <strong>如果你覺得這個專案有幫助，請給個 ⭐ Star！</strong>
</p>
