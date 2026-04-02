# Bleem Box

## English

Bleem Box is a desktop toolbox built with Tkinter. It opens as a single app with multiple utilities inside, and it supports both Chinese and English with a language switch in the top-right corner.

### Tools

- Batch file renaming: rename many files at once with live preview.
- QR code generator: create a QR code from a link and save it as a PNG.
- PDF text scanner: extract text from PDFs page by page and fall back to OCR for scanned pages.
- Mouse cursor skins: apply a single cursor file, apply a full cursor skin folder, test starter presets, or reset back to the default Windows cursor skin.

### Requirements

- Python 3.10+
- Windows is recommended for the full feature set.
- The mouse cursor skin tool only works on Windows.

### Run The App
```powershell
python main.py
```

You can also run it from the project root:

```powershell
python BleemBox/main.py
```

### Dependency Install

`main.py` checks for missing packages before the UI loads. If something required is missing, it tries to install packages from `requirements.txt` automatically.

Current dependencies include:

- `qrcode[pil]`
- `pypdf`
- `pypdfium2`
- Windows OCR packages on Windows
- `rapidocr-onnxruntime` on supported non-Windows Python versions

### Notes

- The PDF tool extracts embedded text first and only uses OCR when needed.
- OCR quality depends on the PDF scan quality.
- The cursor reset button restores the default Windows cursor files from the system cursor folder.
- Changing the language rebuilds the interface so labels update immediately.

### Project Files

- `main.py`: launcher and dependency check
- `app.py`: main window, layout, and navigation
- `requirements.txt`: Python package requirements

---

## 中文

Bleem Box 是一个使用 Tkinter 构建的桌面工具箱。它会以一个应用的形式打开，并在内部集成多个小工具，同时支持中文和英文，可在右上角切换语言。

### 工具功能

- 批量文件重命名：支持一次重命名多个文件，并实时预览结果。
- 二维码生成器：可根据链接生成二维码，并保存为 PNG。
- PDF 文本扫描：按页提取 PDF 文本，遇到扫描版页面时会自动回退到 OCR。
- 鼠标指针皮肤：支持应用单个指针文件、整个皮肤文件夹、测试内置预设，以及恢复为 Windows 默认指针皮肤。

### 运行要求

- Python 3.10 及以上
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

`main.py` 会在界面加载前检查缺失依赖。如果发现缺少必须的包，它会尝试根据 `requirements.txt` 自动安装。

当前依赖包括：

- `qrcode[pil]`
- `pypdf`
- `pypdfium2`
- Windows 下使用的 Windows OCR 相关包
- 在受支持的非 Windows Python 版本上使用的 `rapidocr-onnxruntime`

### 说明

- PDF 工具会优先提取内嵌文本，只有在需要时才会使用 OCR。
- OCR 效果取决于 PDF 扫描质量。
- 指针工具中的恢复按钮会把鼠标指针恢复为系统默认的 Windows 指针文件。
- 切换语言时，界面会重建一次，以便立即更新所有文字。

### 主要文件

- `main.py`：启动器与依赖检查
- `app.py`：主窗口、布局与页面导航
- `requirements.txt`：Python 依赖列表
