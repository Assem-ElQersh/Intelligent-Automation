"""
Lab 01 — File & Folder Automation
Core classification logic: maps file extensions to category folders.
"""

FILE_TYPE_MAP = {
    # Documents
    ".pdf": "documents",
    ".doc": "documents",
    ".docx": "documents",
    ".txt": "documents",
    ".odt": "documents",
    ".rtf": "documents",
    # Spreadsheets
    ".xls": "spreadsheets",
    ".xlsx": "spreadsheets",
    ".csv": "spreadsheets",
    ".ods": "spreadsheets",
    # Images
    ".jpg": "images",
    ".jpeg": "images",
    ".png": "images",
    ".gif": "images",
    ".bmp": "images",
    ".tiff": "images",
    ".webp": "images",
    ".svg": "images",
    # Audio
    ".mp3": "audio",
    ".wav": "audio",
    ".flac": "audio",
    ".aac": "audio",
    ".ogg": "audio",
    # Video
    ".mp4": "video",
    ".avi": "video",
    ".mkv": "video",
    ".mov": "video",
    ".wmv": "video",
    # Archives
    ".zip": "archives",
    ".tar": "archives",
    ".gz": "archives",
    ".rar": "archives",
    ".7z": "archives",
    # Code
    ".py": "code",
    ".js": "code",
    ".ts": "code",
    ".html": "code",
    ".css": "code",
    ".java": "code",
    ".cpp": "code",
    ".c": "code",
    ".sh": "code",
    ".json": "code",
    ".xml": "code",
    ".yaml": "code",
    ".yml": "code",
}


def classify_file(extension: str) -> str:
    """Return the category folder name for a given file extension."""
    return FILE_TYPE_MAP.get(extension.lower(), "other")
