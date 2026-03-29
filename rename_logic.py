from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class RenamePreview:
    # One preview item keeps the old and new file information together.
    original_name: str
    new_name: str
    path: Path
    new_path: Path


def _sorted_files(paths: Iterable[str | Path]) -> list[Path]:
    files = [Path(path) for path in paths if Path(path).is_file()]
    return sorted(files, key=lambda item: item.name.lower())


def build_rename_preview(
    paths: Iterable[str | Path],
    base_name: str,
    start_number: int = 1,
    keep_extension: bool = True,
) -> list[RenamePreview]:
    # Build the list shown in the UI before any real rename happens.
    cleaned_name = base_name.strip()
    if not cleaned_name:
        raise ValueError("Base name is required.")

    files = _sorted_files(paths)
    if not files:
        raise ValueError("Choose at least one file.")

    preview: list[RenamePreview] = []
    for index, path in enumerate(files, start=start_number):
        suffix = path.suffix if keep_extension else ""
        new_name = f"{cleaned_name}_{index}{suffix}"
        preview.append(
            RenamePreview(
                original_name=path.name,
                new_name=new_name,
                path=path,
                new_path=path.with_name(new_name),
            )
        )
    return preview


def validate_preview(preview: Iterable[RenamePreview]) -> None:
    # Catch name collisions before touching the files on disk.
    rename_items = list(preview)
    if not rename_items:
        raise ValueError("Nothing to rename.")

    seen_names: set[str] = set()
    original_paths = {item.path.resolve() for item in rename_items}

    for item in rename_items:
        lowered_name = item.new_name.lower()
        if lowered_name in seen_names:
            raise ValueError(f"Duplicate new name found: {item.new_name}")
        seen_names.add(lowered_name)

        target_path = item.new_path.resolve()
        if target_path.exists() and target_path not in original_paths:
            raise ValueError(f"Target file already exists: {item.new_name}")


def rename_files(preview: Iterable[RenamePreview]) -> int:
    rename_items = list(preview)
    validate_preview(rename_items)

    temp_moves: list[tuple[Path, Path]] = []
    final_moves: list[tuple[Path, Path]] = []

    for index, item in enumerate(rename_items):
        if item.path.resolve() == item.new_path.resolve():
            continue

        # Use temporary names first so swaps and overlapping rename targets work safely.
        temp_path = item.path.with_name(f".__rename_tmp__{index}_{item.path.name}")
        while temp_path.exists():
            temp_path = temp_path.with_name(f".__rename_tmp__{index + 1}_{item.path.name}")
        temp_moves.append((item.path, temp_path))
        final_moves.append((temp_path, item.new_path))

    for original_path, temp_path in temp_moves:
        original_path.rename(temp_path)

    renamed_count = 0
    try:
        for temp_path, final_path in final_moves:
            temp_path.rename(final_path)
            renamed_count += 1
    except Exception:
        # If anything fails midway, move files back so the folder is not left half-renamed.
        for temp_path, final_path in final_moves:
            if final_path.exists() and not temp_path.exists():
                final_path.rename(temp_path)
        for original_path, temp_path in reversed(temp_moves):
            if temp_path.exists():
                temp_path.rename(original_path)
        raise

    return renamed_count
