# Bleem Box

## English

Bleem Box is a desktop toolbox built with Tkinter. It opens as one app and lets you jump into multiple small utilities from a single home screen.

The interface supports both English and Chinese, includes a language switch in the top-right corner, and uses scrollable layouts so tools stay usable even when there are many sections on screen.

### Current Tools

- Batch file renaming
  Rename many files at once with live preview.
- QR code generator
  Create a QR code from a link and save it as a PNG image.
- PDF text scanner
  Extract text from PDFs page by page and fall back to OCR for scanned pages.
- PDF merge tool
  Choose multiple PDFs, remove unwanted pages from each file, then merge the remaining pages into one new PDF.
- Mouse cursor skins
  Apply a single cursor file, apply a full cursor skin folder, test starter presets, or reset back to the default Windows cursor skin.

### Main Features

- One toolbox window with built-in navigation
- Scrollable home screen with quick-jump buttons
- Chinese and English UI
- Automatic dependency check on startup
- Cleaner high-DPI rendering on Windows

### Requirements

- Python 3.10+
- Windows is recommended for the full feature set
- The mouse cursor skin tool only works on Windows

### Run The App

From the `BleemBox` folder:

```powershell
python main.py
```

You can also run it from the project root:

```powershell
python BleemBox/main.py
```

### Dependency Install

`main.py` checks for missing packages before the full UI loads. If something required is missing, it tries to install packages from `requirements.txt` automatically.

Current dependencies:

- `qrcode[pil]`
- `pypdf`
- `pypdfium2`
- Windows OCR packages on Windows
- `rapidocr-onnxruntime` on supported non-Windows Python versions

### Notes

- The PDF text tool extracts embedded text first and only uses OCR when needed.
- The PDF merge tool creates a new PDF and does not overwrite the original files.
- OCR quality depends on the scan quality of the PDF.
- Changing the language rebuilds the interface so labels update immediately.

---

## 中文

Bleem Box 是一个用 Tkinter 制作的桌面工具箱。它会以一个应用的形式打开，并在同一个主界面里提供多个小工具，方便你快速切换使用。

界面支持中文和英文，可以在右上角切换语言。主页和较长的工具页面都支持滚动，这样就算工具越来越多，也不用把窗口拉得很大才能看到全部内容。

### 当前工具

- 批量文件重命名
  可一次性重命名多个文件，并实时预览结果。
- 二维码生成器
  可根据链接生成二维码，并保存为 PNG 图片。
- PDF 文字提取
  可按页提取 PDF 中的文字，遇到扫描版页面时会自动使用 OCR。
- PDF 合并工具
  可选择多个 PDF，先删除每个文件里不需要的页面，再把剩余页面合并成一个新的 PDF。
- 鼠标指针皮肤
  支持应用单个指针文件、整套指针皮肤文件夹、测试内置预设，以及恢复默认 Windows 指针。

### 主要功能

- 一个窗口内集中管理多个工具
- 可滚动的主页，并带有快捷跳转按钮
- 中英文双语界面
- 启动时自动检查依赖
- 在 Windows 上支持更清晰的高 DPI 显示

### 运行要求

- Python 3.10 或以上
- 建议在 Windows 上使用，以获得完整功能
- 鼠标指针皮肤工具仅支持 Windows

### 运行方式

在 `BleemBox` 文件夹中运行：

```powershell
python main.py
```

也可以在项目根目录运行：

```powershell
python BleemBox/main.py
```

### 依赖安装

`main.py` 会在完整界面加载前检查缺失依赖。如果发现缺少必须的包，它会根据 `requirements.txt` 自动尝试安装。

当前依赖包括：

- `qrcode[pil]`
- `pypdf`
- `pypdfium2`
- Windows 下使用的 Windows OCR 相关包
- 在受支持的非 Windows Python 版本中使用的 `rapidocr-onnxruntime`

### 说明

- PDF 文字提取工具会优先读取 PDF 内嵌文字，只有在需要时才使用 OCR。
- PDF 合并工具会生成一个新的 PDF，不会覆盖原始文件。
- OCR 效果会受到 PDF 扫描质量影响。
- 切换语言后，界面会立即重建并更新文字内容。
