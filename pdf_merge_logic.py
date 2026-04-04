from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path
from typing import Iterable

from pypdf import PdfReader, PdfWriter

from i18n import t


@dataclass(frozen=True)
class PDFMergeItem:
    """One selected PDF plus the pages the user wants to leave out."""

    path: Path
    total_pages: int
    removed_pages: frozenset[int] = frozenset()
    removed_pages_text: str = ""

    @property
    def kept_pages(self) -> int:
        return self.total_pages - len(self.removed_pages)


def _as_pdf_path(path: str | Path) -> Path:
    pdf_path = Path(path)
    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError(t("logic.pdf_merge.invalid_pdf", name=pdf_path.name))
    if not pdf_path.is_file():
        raise ValueError(t("logic.pdf_merge.not_found", name=pdf_path.name))
    return pdf_path


def load_pdf_merge_items(paths: Iterable[str | Path]) -> list[PDFMergeItem]:
    """Load each PDF and record how many pages it contains."""
    items: list[PDFMergeItem] = []

    for raw_path in paths:
        pdf_path = _as_pdf_path(raw_path)
        reader = PdfReader(str(pdf_path))
        total_pages = len(reader.pages)
        if total_pages == 0:
            raise ValueError(t("logic.pdf_merge.no_pages", name=pdf_path.name))

        items.append(PDFMergeItem(path=pdf_path, total_pages=total_pages))

    if not items:
        raise ValueError(t("logic.pdf_merge.choose_files"))

    return items


def parse_removed_pages(text: str, total_pages: int) -> tuple[frozenset[int], str]:
    """Turn input like '2, 5-7' into a validated set of 1-based page numbers."""
    cleaned_text = text.strip()
    if not cleaned_text:
        return frozenset(), ""

    removed_pages: set[int] = set()
    parts = [part.strip() for part in cleaned_text.split(",") if part.strip()]

    if not parts:
        return frozenset(), ""

    for part in parts:
        if "-" in part:
            start_text, end_text = [piece.strip() for piece in part.split("-", 1)]
            if not start_text or not end_text:
                raise ValueError(t("logic.pdf_merge.invalid_range", value=part))

            try:
                start_page = int(start_text)
                end_page = int(end_text)
            except ValueError as exc:
                raise ValueError(t("logic.pdf_merge.invalid_range", value=part)) from exc

            if start_page > end_page:
                raise ValueError(t("logic.pdf_merge.range_order", value=part))

            for page_number in range(start_page, end_page + 1):
                if page_number < 1 or page_number > total_pages:
                    raise ValueError(t("logic.pdf_merge.invalid_page", page=page_number, total=total_pages))
                removed_pages.add(page_number)
            continue

        try:
            page_number = int(part)
        except ValueError as exc:
            raise ValueError(t("logic.pdf_merge.invalid_page_value", value=part)) from exc

        if page_number < 1 or page_number > total_pages:
            raise ValueError(t("logic.pdf_merge.invalid_page", page=page_number, total=total_pages))
        removed_pages.add(page_number)

    normalized_text = ", ".join(_compress_page_numbers(sorted(removed_pages)))
    return frozenset(removed_pages), normalized_text


def _compress_page_numbers(page_numbers: list[int]) -> list[str]:
    if not page_numbers:
        return []

    ranges: list[str] = []
    start = page_numbers[0]
    end = page_numbers[0]

    for page_number in page_numbers[1:]:
        if page_number == end + 1:
            end = page_number
            continue

        ranges.append(str(start) if start == end else f"{start}-{end}")
        start = end = page_number

    ranges.append(str(start) if start == end else f"{start}-{end}")
    return ranges


def update_removed_pages(item: PDFMergeItem, text: str) -> PDFMergeItem:
    """Return a new merge item with an updated remove-page plan."""
    removed_pages, normalized_text = parse_removed_pages(text, item.total_pages)
    return replace(item, removed_pages=removed_pages, removed_pages_text=normalized_text)


def merge_pdf_items(items: Iterable[PDFMergeItem], output_path: str | Path) -> int:
    """Build one new PDF from the kept pages of each selected input file."""
    merge_items = list(items)
    if not merge_items:
        raise ValueError(t("logic.pdf_merge.choose_files"))

    writer = PdfWriter()
    pages_written = 0

    for item in merge_items:
        reader = PdfReader(str(item.path))
        for page_number, page in enumerate(reader.pages, start=1):
            if page_number in item.removed_pages:
                continue
            writer.add_page(page)
            pages_written += 1

    if pages_written == 0:
        raise ValueError(t("logic.pdf_merge.no_output_pages"))

    output_file = Path(output_path)
    with output_file.open("wb") as handle:
        writer.write(handle)

    return pages_written


def merge_summary(items: Iterable[PDFMergeItem]) -> tuple[int, int]:
    """Return the number of selected PDFs and the total pages that will remain."""
    merge_items = list(items)
    return len(merge_items), sum(item.kept_pages for item in merge_items)
