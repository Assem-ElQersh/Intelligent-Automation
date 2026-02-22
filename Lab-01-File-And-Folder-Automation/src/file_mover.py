"""
Lab 01 — File & Folder Automation
Handles moving a file to its classified destination and logging the action.
"""

import csv
import shutil
from datetime import datetime
from pathlib import Path

from classifier import classify_file


LOG_COLUMNS = ["timestamp", "original_name", "extension", "category", "destination", "status"]


def _ensure_log(log_path: Path) -> None:
    if not log_path.exists():
        with open(log_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=LOG_COLUMNS)
            writer.writeheader()


def _append_log(log_path: Path, record: dict) -> None:
    with open(log_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=LOG_COLUMNS)
        writer.writerow(record)


def move_file(source: Path, sorted_root: Path, log_path: Path) -> None:
    """
    Move `source` into the appropriate category subfolder under `sorted_root`,
    rename it with a timestamp prefix, and append an entry to the CSV audit log.
    """
    _ensure_log(log_path)

    extension = source.suffix
    category = classify_file(extension)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_name = f"{timestamp}_{source.name}"

    dest_folder = sorted_root / category
    dest_folder.mkdir(parents=True, exist_ok=True)
    dest_path = dest_folder / new_name

    # Avoid overwriting if a file with the same timestamped name exists
    counter = 1
    while dest_path.exists():
        new_name = f"{timestamp}_{counter}_{source.name}"
        dest_path = dest_folder / new_name
        counter += 1

    status = "ok"
    try:
        shutil.move(str(source), str(dest_path))
    except Exception as exc:
        status = f"error: {exc}"

    _append_log(log_path, {
        "timestamp": datetime.now().isoformat(),
        "original_name": source.name,
        "extension": extension if extension else "(none)",
        "category": category,
        "destination": str(dest_path),
        "status": status,
    })

    print(f"[{'OK' if status == 'ok' else 'ERR'}] {source.name} → {category}/{new_name}")
