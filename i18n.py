from __future__ import annotations


LANGUAGE_LABELS = {
    "en": "English",
    "zh": "中文",
}

_current_language = "zh"

TRANSLATIONS = {
    "app.window_title": {
        "en": "Bleem Box",
        "zh": "Bleem Box",
    },
    "app.sidebar_badge": {
        "en": "Desktop toolbox",
        "zh": "桌面工具箱",
    },
    "app.sidebar_subtitle": {
        "en": "Clean utilities for quick desktop tasks.",
        "zh": "把常用桌面小工具放进一个更整洁、更顺手的工作区。",
    },
    "app.nav_home": {
        "en": "Home",
        "zh": "主页",
    },
    "app.nav_renamer": {
        "en": "Batch file renaming",
        "zh": "批量重命名",
    },
    "app.nav_qr": {
        "en": "QR code generator",
        "zh": "二维码生成器",
    },
    "app.nav_pdf": {
        "en": "PDF text scanner",
        "zh": "PDF 文本扫描",
    },
    "app.nav_cursor": {
        "en": "Mouse cursor skins",
        "zh": "鼠标指针皮肤",
    },
    "app.language": {
        "en": "Language",
        "zh": "语言",
    },
    "home.title": {
        "en": "Pick the utility you want to open.",
        "zh": "选择你要打开的工具。",
    },
    "home.subtitle": {
        "en": "Each card opens directly into its workspace with the same updated design system across the app.",
        "zh": "每张卡片都会直接打开对应工具，并保持整套界面风格一致。",
    },
    "home.open_tool": {
        "en": "Open Tool",
        "zh": "打开工具",
    },
    "home.card_renamer_title": {
        "en": "Batch File Renaming",
        "zh": "批量文件重命名",
    },
    "home.card_renamer_text": {
        "en": "Rename many files at once with a simple base name and instant preview.",
        "zh": "输入一个基础名称，马上预览并一次性重命名多个文件。",
    },
    "home.card_qr_title": {
        "en": "QR Code Generator",
        "zh": "二维码生成器",
    },
    "home.card_qr_text": {
        "en": "Generate a QR code for a website, image link, or music link, then save it as a PNG.",
        "zh": "为网页、图片链接或音乐链接生成二维码，并保存为 PNG。",
    },
    "home.card_pdf_title": {
        "en": "PDF Text Scanner",
        "zh": "PDF 文本扫描",
    },
    "home.card_pdf_text": {
        "en": "Extract readable text from every PDF page, keep page breaks, and save the result as a TXT file.",
        "zh": "提取 PDF 每一页中的可读文本，保留分页，并保存为 TXT 文件。",
    },
    "home.card_cursor_title": {
        "en": "Mouse Cursor Skins",
        "zh": "鼠标指针皮肤",
    },
    "home.card_cursor_text": {
        "en": "Test built-in cursor presets, load your own .cur file, or apply a full folder-based cursor skin pack.",
        "zh": "测试内置指针预设、加载你自己的 .cur 文件，或应用整个文件夹形式的指针皮肤包。",
    },
    "common.back_home": {
        "en": "Back to Home",
        "zh": "返回主页",
    },
    "renamer.title": {
        "en": "Rename Multiple Files",
        "zh": "重命名多个文件",
    },
    "renamer.subtitle": {
        "en": "Select files, preview the new names, then rename everything in one step.",
        "zh": "选择文件，先查看新名称预览，再一步完成全部重命名。",
    },
    "renamer.status_initial": {
        "en": "Choose files to start.",
        "zh": "先选择要处理的文件。",
    },
    "renamer.label_files": {
        "en": "Files",
        "zh": "文件",
    },
    "renamer.choose_files": {
        "en": "Choose Files",
        "zh": "选择文件",
    },
    "renamer.label_base_name": {
        "en": "Base name",
        "zh": "基础名称",
    },
    "renamer.default_base_name": {
        "en": "file",
        "zh": "文件",
    },
    "renamer.label_start_number": {
        "en": "Start number",
        "zh": "起始编号",
    },
    "renamer.keep_extensions": {
        "en": "Keep file extensions",
        "zh": "保留文件扩展名",
    },
    "renamer.rename_files": {
        "en": "Rename Files",
        "zh": "重命名文件",
    },
    "renamer.preview": {
        "en": "Preview",
        "zh": "预览",
    },
    "renamer.current_name": {
        "en": "Current Name",
        "zh": "当前名称",
    },
    "renamer.new_name": {
        "en": "New Name",
        "zh": "新名称",
    },
    "renamer.choose_files_dialog": {
        "en": "Choose files to rename",
        "zh": "选择要重命名的文件",
    },
    "renamer.start_number_whole": {
        "en": "Start number must be a whole number.",
        "zh": "起始编号必须是整数。",
    },
    "renamer.start_number_positive": {
        "en": "Start number must be 1 or higher.",
        "zh": "起始编号必须大于或等于 1。",
    },
    "renamer.selected_count": {
        "en": "{count} file(s) selected.",
        "zh": "已选择 {count} 个文件。",
    },
    "renamer.preview_ready": {
        "en": "Preview ready for {count} file(s).",
        "zh": "已为 {count} 个文件生成预览。",
    },
    "renamer.confirm_rename": {
        "en": "Rename {count} file(s)?",
        "zh": "要重命名 {count} 个文件吗？",
    },
    "renamer.rename_failed": {
        "en": "Rename failed:\n{error}",
        "zh": "重命名失败：\n{error}",
    },
    "renamer.renamed_success": {
        "en": "Renamed {count} file(s) successfully.",
        "zh": "已成功重命名 {count} 个文件。",
    },
    "renamer.renamed_info": {
        "en": "Renamed {count} file(s).",
        "zh": "已重命名 {count} 个文件。",
    },
    "qr.title": {
        "en": "QR Code Generator",
        "zh": "二维码生成器",
    },
    "qr.subtitle": {
        "en": "Paste a link to a website page, then generate a QR code to share and scan.",
        "zh": "粘贴网页链接，然后生成可分享、可扫码的二维码。",
    },
    "qr.status_initial": {
        "en": "Paste a link to generate a QR code.",
        "zh": "粘贴链接后即可生成二维码。",
    },
    "qr.label_link": {
        "en": "Link",
        "zh": "链接",
    },
    "qr.link_help": {
        "en": "Use any link that opens a website, image, playlist, song, or video.",
        "zh": "可以使用网页、图片、歌单、歌曲或视频等任意可打开的链接。",
    },
    "qr.website_example": {
        "en": "Website Example",
        "zh": "网站示例",
    },
    "qr.generate": {
        "en": "Generate QR Code",
        "zh": "生成二维码",
    },
    "qr.save_png": {
        "en": "Save PNG",
        "zh": "保存 PNG",
    },
    "qr.preview": {
        "en": "QR Preview",
        "zh": "二维码预览",
    },
    "qr.preview_placeholder": {
        "en": "Your QR code will appear here.",
        "zh": "你的二维码会显示在这里。",
    },
    "qr.ready": {
        "en": "QR code ready. Save it as a PNG or scan it now.",
        "zh": "二维码已生成。你可以立即保存为 PNG 或直接扫码。",
    },
    "qr.generate_first": {
        "en": "Generate a QR code first.",
        "zh": "请先生成二维码。",
    },
    "qr.save_dialog": {
        "en": "Save QR Code",
        "zh": "保存二维码",
    },
    "qr.saved_status": {
        "en": "Saved QR code to {name}.",
        "zh": "二维码已保存到 {name}。",
    },
    "qr.saved_info": {
        "en": "Saved QR code to:\n{path}",
        "zh": "二维码已保存到：\n{path}",
    },
    "dialog.filetype_png": {
        "en": "PNG Image",
        "zh": "PNG 图片",
    },
    "dialog.filetype_text": {
        "en": "Text Files",
        "zh": "文本文件",
    },
    "dialog.filetype_pdf": {
        "en": "PDF Files",
        "zh": "PDF 文件",
    },
    "dialog.filetype_cursor": {
        "en": "Cursor Files",
        "zh": "指针文件",
    },
    "pdf.title": {
        "en": "PDF Text Scanner",
        "zh": "PDF 文本扫描",
    },
    "pdf.subtitle": {
        "en": "Open a PDF, extract the full text page by page, and use OCR automatically when a page is scanned.",
        "zh": "打开 PDF，逐页提取完整文本；如果页面是扫描图像，会自动使用 OCR。",
    },
    "pdf.status_initial": {
        "en": "Choose a PDF to scan its text.",
        "zh": "选择一个 PDF 开始扫描文本。",
    },
    "pdf.no_file": {
        "en": "No PDF selected yet.",
        "zh": "还没有选择 PDF。",
    },
    "pdf.selected_pdf": {
        "en": "Selected PDF",
        "zh": "已选择的 PDF",
    },
    "pdf.choose_pdf": {
        "en": "Choose PDF",
        "zh": "选择 PDF",
    },
    "pdf.extract_text": {
        "en": "Extract Text",
        "zh": "提取文本",
    },
    "pdf.save_txt": {
        "en": "Save TXT",
        "zh": "保存 TXT",
    },
    "pdf.extracted_text": {
        "en": "Extracted Text",
        "zh": "提取结果",
    },
    "pdf.choose_dialog": {
        "en": "Choose PDF",
        "zh": "选择 PDF",
    },
    "pdf.choose_first": {
        "en": "Choose a PDF first.",
        "zh": "请先选择 PDF。",
    },
    "pdf.extract_failed": {
        "en": "Could not extract text:\n{error}",
        "zh": "无法提取文本：\n{error}",
    },
    "pdf.extracted_status": {
        "en": "Extracted text from {name}.",
        "zh": "已从 {name} 提取文本。",
    },
    "pdf.extract_first": {
        "en": "Extract text from a PDF first.",
        "zh": "请先从 PDF 中提取文本。",
    },
    "pdf.save_dialog": {
        "en": "Save Extracted Text",
        "zh": "保存提取文本",
    },
    "pdf.saved_status": {
        "en": "Saved extracted text to {name}.",
        "zh": "提取文本已保存到 {name}。",
    },
    "pdf.saved_info": {
        "en": "Saved extracted text to:\n{path}",
        "zh": "提取文本已保存到：\n{path}",
    },
    "cursor.title": {
        "en": "Mouse Cursor Skins",
        "zh": "鼠标指针皮肤",
    },
    "cursor.subtitle": {
        "en": "Apply a starter cursor, use your own .cur or .ani file, or load a full folder-based cursor skin pack.",
        "zh": "应用内置指针、使用你自己的 .cur / .ani 文件，或加载整个文件夹形式的指针皮肤包。",
    },
    "cursor.windows_only": {
        "en": "This tool only works on Windows because it updates the system cursor settings.",
        "zh": "这个工具仅支持 Windows，因为它会修改系统鼠标指针设置。",
    },
    "cursor.status_initial": {
        "en": "Pick a starter preset or load your own cursor skin.",
        "zh": "选择一个预设，或加载你自己的指针皮肤。",
    },
    "cursor.no_custom_file": {
        "en": "No custom cursor file selected.",
        "zh": "还没有选择自定义指针文件。",
    },
    "cursor.no_skin_folder": {
        "en": "No skin folder selected.",
        "zh": "还没有选择皮肤文件夹。",
    },
    "cursor.custom_skin": {
        "en": "Your Own Skin",
        "zh": "你的自定义皮肤",
    },
    "cursor.custom_skin_help": {
        "en": "Use one cursor file for the main arrow, or point to a folder that contains a full skin pack.",
        "zh": "你可以用单个指针文件替换主箭头，也可以选择包含完整皮肤包的文件夹。",
    },
    "cursor.selected_cursor_file": {
        "en": "Selected cursor file",
        "zh": "已选择的指针文件",
    },
    "cursor.choose_cursor_file": {
        "en": "Choose Cursor File",
        "zh": "选择指针文件",
    },
    "cursor.apply_file": {
        "en": "Apply File",
        "zh": "应用文件",
    },
    "cursor.selected_skin_folder": {
        "en": "Selected skin folder",
        "zh": "已选择的皮肤文件夹",
    },
    "cursor.choose_skin_folder": {
        "en": "Choose Skin Folder",
        "zh": "选择皮肤文件夹",
    },
    "cursor.apply_folder": {
        "en": "Apply Folder",
        "zh": "应用文件夹",
    },
    "cursor.reset_default": {
        "en": "Reset to Default",
        "zh": "恢复默认",
    },
    "cursor.starter_presets": {
        "en": "Starter Presets",
        "zh": "预设皮肤",
    },
    "cursor.starter_help": {
        "en": "Click any preview to apply it right away. These presets use cursor files already available on your Windows install.",
        "zh": "点击任意预览图就能立刻应用。这些预设使用的是你当前 Windows 系统里已有的指针文件。",
    },
    "cursor.no_presets": {
        "en": "No starter cursor presets were found on this computer.",
        "zh": "在这台电脑上没有找到可用的预设指针。",
    },
    "cursor.choose_file_dialog": {
        "en": "Choose Cursor File",
        "zh": "选择指针文件",
    },
    "cursor.file_selected_status": {
        "en": "Custom cursor file selected. Apply it when you are ready.",
        "zh": "已选择自定义指针文件，你可以随时应用。",
    },
    "cursor.choose_file_first": {
        "en": "Choose a cursor file first.",
        "zh": "请先选择一个指针文件。",
    },
    "cursor.confirm_apply_file": {
        "en": "Apply this file as your main mouse cursor now?",
        "zh": "现在将这个文件应用为主鼠标指针吗？",
    },
    "cursor.apply_file_failed": {
        "en": "Could not apply cursor file:\n{error}",
        "zh": "无法应用指针文件：\n{error}",
    },
    "cursor.choose_folder_dialog": {
        "en": "Choose Cursor Skin Folder",
        "zh": "选择指针皮肤文件夹",
    },
    "cursor.folder_selected_status": {
        "en": "Cursor skin folder selected. Apply it when you are ready.",
        "zh": "已选择指针皮肤文件夹，你可以随时应用。",
    },
    "cursor.choose_folder_first": {
        "en": "Choose a cursor skin folder first.",
        "zh": "请先选择一个指针皮肤文件夹。",
    },
    "cursor.confirm_apply_folder": {
        "en": "Apply the cursor files found in this folder to Windows now?",
        "zh": "现在将这个文件夹中的指针文件应用到 Windows 吗？",
    },
    "cursor.apply_folder_failed": {
        "en": "Could not apply cursor skin folder:\n{error}",
        "zh": "无法应用指针皮肤文件夹：\n{error}",
    },
    "cursor.confirm_apply_preset": {
        "en": "Apply the starter preset '{name}' as your main cursor now?",
        "zh": "现在将预设“{name}”应用为主鼠标指针吗？",
    },
    "cursor.apply_preset_failed": {
        "en": "Could not apply preset:\n{error}",
        "zh": "无法应用预设：\n{error}",
    },
    "cursor.confirm_reset_default": {
        "en": "Reset the mouse cursor skin back to the default Windows style now?",
        "zh": "现在将鼠标指针皮肤恢复为 Windows 默认样式吗？",
    },
    "cursor.reset_default_failed": {
        "en": "Could not reset the cursor skin:\n{error}",
        "zh": "无法恢复默认指针皮肤：\n{error}",
    },
    "cursor.preset_aero_arrow": {
        "en": "Aero Arrow",
        "zh": "Aero 箭头",
    },
    "cursor.preset_aero_arrow_desc": {
        "en": "Apply the classic Windows aero arrow as your main cursor.",
        "zh": "把经典 Windows Aero 箭头应用为主鼠标指针。",
    },
    "cursor.preset_modern_arrow": {
        "en": "Modern Arrow",
        "zh": "现代箭头",
    },
    "cursor.preset_modern_arrow_desc": {
        "en": "Apply the rounded Windows arrow cursor for a quick test.",
        "zh": "应用更圆润的 Windows 箭头指针，方便快速测试。",
    },
    "cursor.preset_large_arrow": {
        "en": "Large Arrow",
        "zh": "大号箭头",
    },
    "cursor.preset_large_arrow_desc": {
        "en": "Apply a larger cursor so the change is easy to spot right away.",
        "zh": "应用更大的指针，让变化更容易一眼看出来。",
    },
    "cursor.preset_extra_large_arrow": {
        "en": "Extra Large Arrow",
        "zh": "超大箭头",
    },
    "cursor.preset_extra_large_arrow_desc": {
        "en": "Apply an extra large aero cursor for an obvious before-and-after test.",
        "zh": "应用超大的 Aero 指针，方便更明显地对比前后效果。",
    },
    "main.install_error": {
        "en": "The app could not install its required packages automatically.\n\nPlease run:\n{command}\n\nDetails: {error}",
        "zh": "应用无法自动安装所需依赖。\n\n请运行：\n{command}\n\n详细信息：{error}",
    },
    "logic.qr.empty": {
        "en": "Enter a website or direct link first.",
        "zh": "请先输入网站或直接链接。",
    },
    "logic.rename.base_required": {
        "en": "Base name is required.",
        "zh": "必须填写基础名称。",
    },
    "logic.rename.choose_files": {
        "en": "Choose at least one file.",
        "zh": "请至少选择一个文件。",
    },
    "logic.rename.nothing": {
        "en": "Nothing to rename.",
        "zh": "没有可重命名的内容。",
    },
    "logic.rename.duplicate": {
        "en": "Duplicate new name found: {name}",
        "zh": "发现重复的新名称：{name}",
    },
    "logic.rename.exists": {
        "en": "Target file already exists: {name}",
        "zh": "目标文件已存在：{name}",
    },
    "logic.pdf.choose_pdf": {
        "en": "Choose a PDF file first.",
        "zh": "请先选择一个 PDF 文件。",
    },
    "logic.pdf.not_found": {
        "en": "The selected PDF file could not be found.",
        "zh": "找不到所选的 PDF 文件。",
    },
    "logic.pdf.no_pages": {
        "en": "This PDF has no pages to scan.",
        "zh": "这个 PDF 没有可扫描的页面。",
    },
    "logic.pdf.page_header": {
        "en": "----- Page {page} -----",
        "zh": "----- 第 {page} 页 -----",
    },
    "logic.pdf.no_text_details": {
        "en": "[No extractable text found on this page. Details: {details}]",
        "zh": "[这一页没有可提取的文本。详细信息：{details}]",
    },
    "logic.pdf.source_embedded": {
        "en": "embedded PDF text",
        "zh": "PDF 内嵌文本",
    },
    "logic.pdf.source_windows_ocr": {
        "en": "Windows OCR",
        "zh": "Windows OCR",
    },
    "logic.pdf.source_rapidocr": {
        "en": "RapidOCR",
        "zh": "RapidOCR",
    },
    "logic.pdf.windows_only": {
        "en": "Windows OCR is only available on Windows.",
        "zh": "Windows OCR 仅在 Windows 上可用。",
    },
    "logic.pdf.windows_ocr_missing": {
        "en": "Windows OCR packages are not installed.",
        "zh": "未安装 Windows OCR 相关依赖。",
    },
    "logic.pdf.windows_no_text": {
        "en": "Windows OCR ran, but it could not recognize text on the page.",
        "zh": "Windows OCR 已运行，但未识别出页面中的文字。",
    },
    "logic.pdf.windows_failed": {
        "en": "Windows OCR failed: {error}",
        "zh": "Windows OCR 失败：{error}",
    },
    "logic.pdf.rapidocr_missing": {
        "en": "RapidOCR is not installed.",
        "zh": "RapidOCR 未安装。",
    },
    "logic.pdf.rapidocr_failed": {
        "en": "RapidOCR failed: {error}",
        "zh": "RapidOCR 失败：{error}",
    },
    "logic.pdf.rapidocr_no_text": {
        "en": "RapidOCR ran, but it could not recognize text on the page.",
        "zh": "RapidOCR 已运行，但未识别出页面中的文字。",
    },
    "logic.pdf.rapidocr_cleanup_empty": {
        "en": "RapidOCR returned boxes, but no readable text remained after cleanup.",
        "zh": "RapidOCR 返回了识别框，但清理后没有保留可读文本。",
    },
    "logic.pdf.ocr_no_text": {
        "en": "OCR did not return any text.",
        "zh": "OCR 没有返回任何文本。",
    },
    "logic.pdf.ocr_failed": {
        "en": "OCR failed: {error}",
        "zh": "OCR 失败：{error}",
    },
    "logic.cursor.apply_arrow": {
        "en": "Applied {name} as the main mouse cursor.",
        "zh": "已将 {name} 应用为主鼠标指针。",
    },
    "logic.cursor.invalid_folder": {
        "en": "Choose a valid folder that contains cursor files.",
        "zh": "请选择一个包含指针文件的有效文件夹。",
    },
    "logic.cursor.no_roles_found": {
        "en": "No usable cursor roles were found in that folder. Use common names like 'Normal Select', 'Busy', 'Text Select', 'Link Select', Chinese names like '正常选择', '忙', '文本选择', '链接选择', or the template names like 'arrow', 'wait', 'ibeam', and 'hand'.",
        "zh": "这个文件夹里没有找到可用的指针角色。请使用像“Normal Select”“Busy”“Text Select”“Link Select”这样的常见英文名称，或“正常选择”“忙”“文本选择”“链接选择”等中文名称，也可以使用模板名称，如“arrow”“wait”“ibeam”“hand”。",
    },
    "logic.cursor.apply_folder": {
        "en": "Applied {count} cursor role(s) from {name}.",
        "zh": "已从 {name} 应用 {count} 个指针角色。",
    },
    "logic.cursor.default_restored": {
        "en": "Restored the default Windows cursor skin.",
        "zh": "已恢复 Windows 默认指针皮肤。",
    },
    "logic.cursor.default_missing": {
        "en": "The default Windows cursor files could not be found.",
        "zh": "找不到 Windows 默认指针文件。",
    },
    "logic.cursor.invalid_file": {
        "en": "Choose a valid .cur or .ani cursor file.",
        "zh": "请选择一个有效的 .cur 或 .ani 指针文件。",
    },
    "logic.cursor.invalid_format": {
        "en": "Cursor files must use the .cur or .ani format.",
        "zh": "指针文件必须是 .cur 或 .ani 格式。",
    },
    "logic.cursor.windows_only_runtime": {
        "en": "Mouse cursor skin changes are only supported on Windows.",
        "zh": "鼠标指针皮肤更改仅支持 Windows。",
    },
}


def set_language(language: str) -> None:
    global _current_language
    if language in LANGUAGE_LABELS:
        _current_language = language


def get_language() -> str:
    return _current_language


def t(key: str, **kwargs) -> str:
    values = TRANSLATIONS.get(key, {})
    template = values.get(_current_language) or values.get("en") or key
    if kwargs:
        return template.format(**kwargs)
    return template
