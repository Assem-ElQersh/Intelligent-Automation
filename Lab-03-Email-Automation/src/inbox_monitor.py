"""
Lab 03 — Email Automation
IMAP inbox monitor: reads unseen emails, matches keywords, sends auto-replies.
"""

import imaplib
import email
import uuid
from datetime import datetime
from email.header import decode_header
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

import config
from sender import send_email

TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"
LOG_PATH = Path(__file__).resolve().parent.parent / "logs" / "replies.log"

# Keyword → response config
KEYWORD_RULES = {
    "support": {
        "response_message": "Our support team will review your case and get back to you.",
        "sla_hours": 24,
    },
    "invoice": {
        "response_message": "We have forwarded your invoice query to our finance department.",
        "sla_hours": 48,
    },
    "urgent": {
        "response_message": "Your message has been flagged as urgent and escalated.",
        "sla_hours": 4,
    },
    "feedback": {
        "response_message": "Thank you for your feedback! We value every response.",
        "sla_hours": 72,
    },
}
DEFAULT_RULE = {
    "response_message": "We have received your email and will get back to you shortly.",
    "sla_hours": 48,
}


def _decode_header_value(value: str) -> str:
    parts = decode_header(value)
    decoded = []
    for part, charset in parts:
        if isinstance(part, bytes):
            decoded.append(part.decode(charset or "utf-8", errors="replace"))
        else:
            decoded.append(part)
    return " ".join(decoded)


def _match_keyword(subject: str, body: str) -> tuple[str, dict]:
    combined = (subject + " " + body).lower()
    for keyword, rule in KEYWORD_RULES.items():
        if keyword in combined:
            return keyword, rule
    return "general", DEFAULT_RULE


def _render_auto_reply(sender_name: str, original_subject: str, keyword: str, rule: dict) -> str:
    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    template = env.get_template("auto_reply.html")
    return template.render(
        sender_name=sender_name,
        original_subject=original_subject,
        matched_keyword=keyword,
        response_message=rule["response_message"],
        sla_hours=rule["sla_hours"],
        ref_id=str(uuid.uuid4())[:8].upper(),
    )


def _log(entry: str) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().isoformat()}] {entry}\n")


def check_and_reply(mark_seen: bool = True) -> int:
    """
    Connect to IMAP inbox, find UNSEEN emails, send keyword-based auto-replies.

    Returns:
        Number of emails processed.
    """
    processed = 0

    with imaplib.IMAP4_SSL(config.IMAP_HOST, config.IMAP_PORT) as imap:
        imap.login(config.IMAP_USER, config.IMAP_PASSWORD)
        imap.select("INBOX")

        _, message_ids = imap.search(None, "UNSEEN")
        ids = message_ids[0].split()

        if not ids:
            print("No new emails.")
            return 0

        print(f"Found {len(ids)} unread email(s).")

        for msg_id in ids:
            _, data = imap.fetch(msg_id, "(RFC822)")
            raw = data[0][1]
            msg = email.message_from_bytes(raw)

            subject = _decode_header_value(msg.get("Subject", "(no subject)"))
            from_field = _decode_header_value(msg.get("From", ""))
            sender_email = email.utils.parseaddr(from_field)[1]
            sender_name = email.utils.parseaddr(from_field)[0] or sender_email

            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode("utf-8", errors="replace")
                        break
            else:
                body = msg.get_payload(decode=True).decode("utf-8", errors="replace")

            keyword, rule = _match_keyword(subject, body)
            html_body = _render_auto_reply(sender_name, subject, keyword, rule)

            send_email(
                to=sender_email,
                subject=f"Re: {subject}",
                body_text=rule["response_message"],
                body_html=html_body,
            )

            _log(f"AUTO-REPLY → {sender_email} | keyword={keyword} | subject={subject}")

            if mark_seen:
                imap.store(msg_id, "+FLAGS", "\\Seen")

            processed += 1

    return processed
