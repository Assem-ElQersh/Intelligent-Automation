"""
Lab 03 — Email Automation
Configuration loader from .env file.
"""

import os
from dotenv import load_dotenv

load_dotenv()


def get(key: str, default: str = "") -> str:
    return os.getenv(key, default)


SMTP_HOST = get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(get("SMTP_PORT", "587"))
SMTP_USER = get("SMTP_USER")
SMTP_PASSWORD = get("SMTP_PASSWORD")

IMAP_HOST = get("IMAP_HOST", "imap.gmail.com")
IMAP_PORT = int(get("IMAP_PORT", "993"))
IMAP_USER = get("IMAP_USER")
IMAP_PASSWORD = get("IMAP_PASSWORD")
