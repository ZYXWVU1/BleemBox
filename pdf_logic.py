from __future__ import annotations

import asyncio
from io import BytesIO
import re
import sys
from pathlib import Path

from pypdf import PdfReader
import pypdfium2 as pdfium
from PIL import Image, ImageOps


OCR_RENDER_SCALE = 300 / 72
_rapidocr_engine = None


def _normalize_page_text(text: str) -> str:
    """Clean line breaks so extracted PDF text reads more naturally."""
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    normalized = re.sub(r"(?<=\w)-\n(?=\w)", "", normalized)

    paragraphs: list[str] = []
    for block in re.split(r"\n\s*\n", normalized):
        lines = [re.sub(r"\s+", " ", line).strip() for line in block.splitlines() if line.strip()]
        if lines:
            paragraphs.append(" ".join(lines))

    return "\n\n".join(paragraphs)


def _get_rapidocr_engine():
    global _rapidocr_engine
    if _rapidocr_engine is None:
        from rapidocr_onnxruntime import RapidOCR

        _rapidocr_engine = RapidOCR()
    return _rapidocr_engine


def _ocr_sort_key(item: list | tuple) -> tuple[float, float]:
    box = item[0] if item else None
    if not isinstance(box, (list, tuple)) or not box:
        return (0.0, 0.0)

    try:
        xs = [float(point[0]) for point in box]
        ys = [float(point[1]) for point in box]
    except (TypeError, ValueError, IndexError):
        return (0.0, 0.0)

    return (min(ys), min(xs))


def _ocr_box_height(item: list | tuple) -> float:
    box = item[0] if item else None
    if not isinstance(box, (list, tuple)) or not box:
        return 0.0

    try:
        ys = [float(point[1]) for point in box]
    except (TypeError, ValueError, IndexError):
        return 0.0

    return max(ys) - min(ys)


def _extract_text_with_windows_ocr(image: Image.Image) -> tuple[str, str | None]:
    if sys.platform != "win32":
        return "", "Windows OCR is only available on Windows."

    try:
        from winrt.windows.globalization import Language
        from winrt.windows.graphics.imaging import BitmapPixelFormat, SoftwareBitmap
        from winrt.windows.media.ocr import OcrEngine
        from winrt.windows.storage.streams import DataWriter
    except ImportError:
        return "", "Windows OCR packages are not installed."

    processed_image = image.convert("RGBA")

    async def _recognize() -> str:
        writer = DataWriter()
        writer.write_bytes(processed_image.tobytes())
        bitmap = SoftwareBitmap.create_copy_from_buffer(
            writer.detach_buffer(),
            BitmapPixelFormat.RGBA8,
            processed_image.width,
            processed_image.height,
        )

        engine = OcrEngine.try_create_from_user_profile_languages()
        if engine is None:
            fallback_language = Language("en-US")
            if OcrEngine.is_language_supported(fallback_language):
                engine = OcrEngine.try_create_from_language(fallback_language)

        if engine is None:
            return ""

        result = await engine.recognize_async(bitmap)
        return (result.text or "").strip()

    try:
        text = asyncio.run(_recognize())
        if text:
            return text, None
        return "", "Windows OCR ran, but it could not recognize text on the page."
    except Exception as exc:
        return "", f"Windows OCR failed: {exc}"
    finally:
        processed_image.close()


def _extract_text_with_rapidocr(image: Image.Image) -> tuple[str, str | None]:
    try:
        engine = _get_rapidocr_engine()
    except ImportError:
        return "", "RapidOCR is not installed."

    buffer = BytesIO()
    image.save(buffer, format="PNG")
    try:
        result, _elapsed = engine(buffer.getvalue())
    except Exception as exc:
        return "", f"RapidOCR failed: {exc}"

    if not result:
        return "", "RapidOCR ran, but it could not recognize text on the page."

    ordered_results = sorted(result, key=_ocr_sort_key)

    lines: list[str] = []
    previous_bottom = 0.0
    previous_height = 0.0

    for item in ordered_results:
        if not isinstance(item, (list, tuple)) or len(item) < 2:
            continue

        text = str(item[1]).strip()
        if not text:
            continue

        top, _left = _ocr_sort_key(item)
        height = _ocr_box_height(item)
        gap_threshold = max(previous_height, height, 1.0) * 0.8

        if lines and top - previous_bottom > gap_threshold:
            lines.append("")

        lines.append(text)
        previous_bottom = top + height
        previous_height = height

    normalized_text = _normalize_page_text("\n".join(lines))
    if normalized_text:
        return normalized_text, None
    return "", "RapidOCR returned boxes, but no readable text remained after cleanup."


def _extract_text_with_ocr(pdf_document: pdfium.PdfDocument, page_index: int) -> tuple[str, str]:
    page = pdf_document[page_index]
    rendered_page = page.render(scale=OCR_RENDER_SCALE)
    image = rendered_page.to_pil()
    processed_image = ImageOps.autocontrast(ImageOps.grayscale(image))

    try:
        windows_text, windows_note = _extract_text_with_windows_ocr(processed_image)
        if windows_text:
            return _normalize_page_text(windows_text), "Windows OCR"

        rapidocr_text, rapidocr_note = _extract_text_with_rapidocr(processed_image)
        if rapidocr_text:
            return rapidocr_text, "RapidOCR"

        failure_notes = [note for note in (windows_note, rapidocr_note) if note]
        return "", " | ".join(failure_notes) if failure_notes else "OCR did not return any text."
    finally:
        processed_image.close()
        image.close()


def extract_pdf_text(pdf_path: str | Path) -> str:
    """Extract all text from a PDF and fall back to OCR for scanned pages."""
    path = Path(pdf_path)
    if path.suffix.lower() != ".pdf":
        raise ValueError("Choose a PDF file first.")
    if not path.is_file():
        raise ValueError("The selected PDF file could not be found.")

    reader = PdfReader(str(path))
    if not reader.pages:
        raise ValueError("This PDF has no pages to scan.")

    page_sections: list[str] = []
    pdf_document: pdfium.PdfDocument | None = None
    for page_number, page in enumerate(reader.pages, start=1):
        try:
            raw_text = page.extract_text() or ""
        except Exception:
            raw_text = ""

        page_text = _normalize_page_text(raw_text)
        extraction_source = "embedded PDF text"
        if not page_text:
            if pdf_document is None:
                pdf_document = pdfium.PdfDocument(str(path))
            try:
                page_text, extraction_source = _extract_text_with_ocr(pdf_document, page_number - 1)
            except Exception as exc:
                page_text = ""
                extraction_source = f"OCR failed: {exc}"

        if not page_text:
            page_text = f"[No extractable text found on this page. Details: {extraction_source}]"

        page_sections.append(f"----- Page {page_number} -----\n{page_text}")

    return "\n\n".join(page_sections)
