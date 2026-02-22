"""
Lab 01 — File & Folder Automation
Helper script: generates sample dummy files in data/inbox/ for testing.

Usage:
    python generate_sample_files.py
"""

from pathlib import Path

INBOX = Path(__file__).resolve().parent.parent / "data" / "inbox"

SAMPLE_FILES = [
    "report_q1.pdf",
    "budget_2024.xlsx",
    "profile_photo.jpg",
    "background_music.mp3",
    "demo_video.mp4",
    "archive_backup.zip",
    "script.py",
    "notes.txt",
    "data_dump.csv",
    "logo.png",
    "unknown_file",
]


def main() -> None:
    INBOX.mkdir(parents=True, exist_ok=True)
    for name in SAMPLE_FILES:
        path = INBOX / name
        path.write_text(f"Sample content for {name}\n")
        print(f"Created: {path}")
    print(f"\n{len(SAMPLE_FILES)} sample files created in {INBOX}")


if __name__ == "__main__":
    main()
