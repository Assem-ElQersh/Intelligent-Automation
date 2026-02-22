"""
Lab 01 — File & Folder Automation
Batch mode: classify all existing files in data/inbox/ without the watcher.

Usage:
    python batch_sort.py
"""

from pathlib import Path

from file_mover import move_file

BASE_DIR = Path(__file__).resolve().parent.parent
INBOX_DIR = BASE_DIR / "data" / "inbox"
SORTED_DIR = BASE_DIR / "data" / "sorted"
LOG_PATH = BASE_DIR / "logs" / "audit.csv"


def main() -> None:
    INBOX_DIR.mkdir(parents=True, exist_ok=True)
    SORTED_DIR.mkdir(parents=True, exist_ok=True)
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    files = [f for f in INBOX_DIR.iterdir() if f.is_file()]
    if not files:
        print("Inbox is empty. Add files to data/inbox/ first.")
        return

    print(f"Found {len(files)} file(s) in inbox. Sorting...\n")
    for f in files:
        move_file(f, SORTED_DIR, LOG_PATH)

    print(f"\nDone. Audit log saved to: {LOG_PATH}")


if __name__ == "__main__":
    main()
