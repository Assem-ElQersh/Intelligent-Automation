"""
Lab 01 — File & Folder Automation
Real-time folder watcher using watchdog.
Monitors data/inbox/ and automatically classifies new files.

Usage:
    python watcher.py
"""

import sys
import time
from pathlib import Path

from watchdog.events import FileSystemEventHandler, FileCreatedEvent
from watchdog.observers import Observer

from file_mover import move_file

BASE_DIR = Path(__file__).resolve().parent.parent
INBOX_DIR = BASE_DIR / "data" / "inbox"
SORTED_DIR = BASE_DIR / "data" / "sorted"
LOG_PATH = BASE_DIR / "logs" / "audit.csv"


class InboxHandler(FileSystemEventHandler):
    def on_created(self, event: FileCreatedEvent) -> None:
        if event.is_directory:
            return
        source = Path(event.src_path)
        # Brief wait to ensure the file is fully written before moving
        time.sleep(0.5)
        if source.exists():
            move_file(source, SORTED_DIR, LOG_PATH)


def main() -> None:
    INBOX_DIR.mkdir(parents=True, exist_ok=True)
    SORTED_DIR.mkdir(parents=True, exist_ok=True)
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    print(f"Watching: {INBOX_DIR}")
    print(f"Sorted into: {SORTED_DIR}")
    print(f"Audit log: {LOG_PATH}")
    print("Press Ctrl+C to stop.\n")

    handler = InboxHandler()
    observer = Observer()
    observer.schedule(handler, str(INBOX_DIR), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nWatcher stopped.")
    observer.join()


if __name__ == "__main__":
    main()
