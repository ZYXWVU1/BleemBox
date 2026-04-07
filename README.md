# Bleem Box

## English

Bleem Box is a desktop toolbox built with Tkinter. It opens as one app and gives you multiple utilities from a single home screen, with support for both English and Chinese.

### Current Tools

- Batch file renaming
  Rename many files at once with live preview.
- QR code generator
  Create a QR code from a link and save it as a PNG image.
- PDF text scanner
  Extract text from PDFs page by page and fall back to OCR for scanned pages.
- PDF merge tool
  Load multiple PDFs, remove unwanted pages from each file, then merge the rest into one new PDF.
- Random wheel spinner
  Enter your own choices and spin a wheel to pick one result randomly.
- Multi-website opener
  Create named buttons like `Study` or `Work`, save multiple links on each button, and open the whole set with one click.
- Mouse cursor skins
  Apply a single cursor file, apply a full cursor skin folder, try starter presets, or reset back to the default Windows cursor skin.

### Main Features

- One toolbox window with built-in navigation
- Scrollable home screen and scrollable tool layouts
- English and Chinese language switch
- Automatic dependency check on startup
- Sharper font handling for Chinese on Windows

### Requirements

- Python 3.10+
- Windows is recommended for the full feature set
- The mouse cursor skin tool only works on Windows

### Run The App

From the `BleemBoxTool/BleemBox` folder:

```powershell
python main.py
```

You can also run it from the project root:

```powershell
python BleemBoxTool/BleemBox/main.py
```

### Dependencies

`main.py` checks for missing packages before the full UI loads. If something required is missing, it tries to install packages from `requirements.txt` automatically.

Current dependencies include:

- `qrcode[pil]`
- `pypdf`
- `pypdfium2`
- Windows OCR packages on Windows
- `rapidocr-onnxruntime` on supported non-Windows Python versions

### Notes

- The PDF text tool extracts embedded text first and only uses OCR when needed.
- The PDF merge tool creates a new PDF and does not overwrite the original files.
- OCR quality depends on the scan quality of the PDF.
- The multi-website opener saves its button profiles locally so they stay available after restart.
- Changing the language rebuilds the interface so labels update immediately.

---

## 中文

Bleem Box 是一个使用 Tkinter 制作的桌面工具箱。它会以一个应用的形式打开，并在同一个主界面里提供多个小工具，同时支持英文和中文切换。

### 当前工具

- 批量文件重命名
  可以一次性重命名多个文件，并实时预览结果。
- 二维码生成器
  可以根据链接生成二维码，并保存为 PNG 图片。
- PDF 文本提取
  可以按页提取 PDF 中的文字，遇到扫描版页面时会自动使用 OCR。
- PDF 合并工具
  可以加载多个 PDF，先删除每个文件里不需要的页面，再把剩余页面合并成一个新的 PDF。
- 随机转盘
  可以输入自己的选项并旋转转盘，随机选出一个结果。
- 多网址一键打开
  可以创建像“学习”或“工作”这样的自定义按钮，为每个按钮保存多个链接，并一键打开整组网站。
- 鼠标指针皮肤
  支持应用单个指针文件、整套指针皮肤文件夹、测试内置预设，以及恢复默认 Windows 指针。

### 主要功能

- 一个窗口内集中管理多个工具
- 可滚动的主页和工具页面布局
- 中英文语言切换
- 启动时自动检查依赖
- 在 Windows 上为中文提供更清晰的字体显示

### 运行要求

- Python 3.10 或以上
- 建议在 Windows 上使用，以获得完整功能
- 鼠标指针皮肤工具仅支持 Windows

### 运行方式

在 `BleemBoxTool/BleemBox` 文件夹中运行：

```powershell
python main.py
```

也可以在项目根目录运行：

```powershell
python BleemBoxTool/BleemBox/main.py
```

### 依赖说明

`main.py` 会在完整界面加载前检查缺失依赖。如果发现缺少必须的包，它会尝试根据 `requirements.txt` 自动安装。

当前依赖包括：

- `qrcode[pil]`
- `pypdf`
- `pypdfium2`
- Windows 下使用的 Windows OCR 相关包
- 在受支持的非 Windows Python 版本中使用的 `rapidocr-onnxruntime`

### 说明

- PDF 文本提取工具会优先读取 PDF 内嵌文字，只有在需要时才使用 OCR。
- PDF 合并工具会生成一个新的 PDF，不会覆盖原始文件。
- OCR 效果会受到 PDF 扫描质量影响。
- 多网址一键打开工具会把按钮配置保存在本地，重启后仍会保留。
- 切换语言后，界面会立即重建并更新文字内容。
