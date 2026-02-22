"""
Lab 03 — Email Automation
SMTP email sender supporting plain text, HTML body, and file attachments.
"""

import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path

import config


def send_email(
    to: str | list[str],
    subject: str,
    body_text: str = "",
    body_html: str = "",
    attachments: list[Path] | None = None,
) -> None:
    """
    Send an email via SMTP (TLS).

    Args:
        to: Recipient address or list of addresses.
        subject: Email subject line.
        body_text: Plain-text fallback body.
        body_html: HTML body (preferred if provided).
        attachments: List of file paths to attach.
    """
    if isinstance(to, str):
        to = [to]

    msg = MIMEMultipart("alternative")
    msg["From"] = config.SMTP_USER
    msg["To"] = ", ".join(to)
    msg["Subject"] = subject

    if body_text:
        msg.attach(MIMEText(body_text, "plain"))
    if body_html:
        msg.attach(MIMEText(body_html, "html"))

    for path in (attachments or []):
        path = Path(path)
        mime_type, _ = mimetypes.guess_type(str(path))
        main_type, sub_type = (mime_type or "application/octet-stream").split("/", 1)
        with open(path, "rb") as f:
            part = MIMEBase(main_type, sub_type)
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", "attachment", filename=path.name)
        msg.attach(part)

    with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT) as server:
        server.ehlo()
        server.starttls()
        server.login(config.SMTP_USER, config.SMTP_PASSWORD)
        server.sendmail(config.SMTP_USER, to, msg.as_string())

    print(f"[SENT] To: {', '.join(to)} | Subject: {subject}")
