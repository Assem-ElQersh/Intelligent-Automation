# Lab 03 — Email Automation

**Pillar:** RPA (Robotic Process Automation)  
**Difficulty:** Beginner  
**Estimated Time:** 45–60 minutes

---

## Objective

Build an automated email system that:
- Connects to a live inbox via IMAP and reads unseen emails
- Matches emails against keyword rules and sends HTML auto-replies via SMTP
- Generates and sends scheduled HTML reports with CSV attachments

This demonstrates **automated communication** — a core RPA use case in customer service and operations.

---

## Concepts Covered

| Concept | Description |
|---------|-------------|
| SMTP / IMAP | Programmatic email sending and reading |
| Keyword routing | Rule-based triage of incoming messages |
| HTML templating | Dynamic email bodies with Jinja2 |
| Scheduling | Recurring task execution with `schedule` |
| Attachments | Sending CSV files as email attachments |

---

## Project Structure

```
Lab-03-Email-Automation/
├── README.md
├── requirements.txt
├── .env.example           ← copy to .env and fill credentials
├── src/
│   ├── config.py          # Loads SMTP/IMAP credentials from .env
│   ├── sender.py          # Core SMTP send function
│   ├── inbox_monitor.py   # IMAP reader + auto-reply engine
│   ├── report_sender.py   # HTML report generator + scheduler
│   └── main.py            # CLI entry point
├── templates/
│   ├── auto_reply.html    # Jinja2 HTML auto-reply template
│   └── report.html        # Jinja2 HTML report template
├── data/
│   └── attachments/       # Generated CSV report files stored here
└── logs/
    └── replies.log        # Auto-reply action log
```

---

## Setup

### 1. Install dependencies

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure credentials

```bash
cp .env.example .env
# Edit .env with your email credentials
```

> **Gmail users:** Use an [App Password](https://support.google.com/accounts/answer/185833), not your main account password. Enable IMAP in Gmail settings.

---

## Usage

### Monitor inbox and auto-reply

```bash
cd src
python main.py monitor
```

Checks for UNSEEN emails, matches keywords (`support`, `invoice`, `urgent`, `feedback`), and sends a personalized HTML auto-reply.

### Send a report immediately

```bash
cd src
python main.py report --to you@example.com
```

Generates a weekly sales summary report with a CSV attachment and sends it right away — useful for testing.

### Schedule a weekly report

```bash
cd src
python main.py schedule --to you@example.com --day monday --time 08:00
```

Starts a long-running scheduler that sends the report every Monday at 08:00.

---

## How It Works

```
IMAP Inbox (UNSEEN emails)
        │
        ▼ [inbox_monitor.py]
  Decode subject + body
  Match against keyword rules
        │
        ▼ [Jinja2 template]
  Render HTML auto-reply
        │
        ▼ [sender.py → SMTP]
  Send reply to original sender
  Log to logs/replies.log
```

### Keyword Rules

| Keyword | SLA | Response |
|---------|-----|----------|
| `support` | 24h | Forwarded to support team |
| `invoice` | 48h | Forwarded to finance |
| `urgent` | 4h | Escalated immediately |
| `feedback` | 72h | Feedback acknowledged |
| *(default)* | 48h | Generic acknowledgement |

---

## Extension Challenge

1. Add a new keyword rule for `"refund"` with a 12-hour SLA
2. Add CC/BCC support to the `sender.py` function
3. Parse the report data from a real CSV file instead of generating synthetic data
