# Lab 01 — File & Folder Automation

**Pillar:** RPA (Robotic Process Automation)  
**Difficulty:** Beginner  
**Estimated Time:** 30–45 minutes

---

## Objective

Build an automated file organizer that:
- Monitors a folder (`data/inbox/`) for newly dropped files in real time
- Classifies each file by its extension into a category subfolder
- Renames it with a timestamp prefix
- Appends every action to a CSV audit log (`logs/audit.csv`)

This is a foundational RPA pattern: **detect → classify → act → log**.

---

## Concepts Covered

| Concept | Description |
|---------|-------------|
| File system events | Detecting file creation using `watchdog` |
| Rule-based routing | Mapping extensions to categories |
| Audit trails | Logging every automated action with metadata |
| Batch processing | Processing existing files without live monitoring |

---

## Project Structure

```
Lab-01-File-And-Folder-Automation/
├── README.md
├── requirements.txt
├── src/
│   ├── classifier.py          # Extension → category mapping
│   ├── file_mover.py          # Move + rename + log logic
│   ├── watcher.py             # Real-time folder monitor (main entry point)
│   ├── batch_sort.py          # One-shot batch classifier
│   └── generate_sample_files.py  # Creates test files in inbox
├── data/
│   ├── inbox/                 # Drop files here
│   └── sorted/                # Classified files land here
│       ├── documents/
│       ├── images/
│       ├── spreadsheets/
│       └── ...
└── logs/
    └── audit.csv              # Auto-generated action log
```

---

## Setup

```bash
# From the lab directory
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## Usage

### Option A: Real-Time Watcher

Start the watcher, then drop files into `data/inbox/`:

```bash
cd src
python watcher.py
```

The watcher runs indefinitely. Press `Ctrl+C` to stop.

### Option B: Batch Sort

Sort all files already sitting in `data/inbox/`:

```bash
cd src
python batch_sort.py
```

### Generating Test Files

To create sample dummy files for quick testing:

```bash
cd src
python generate_sample_files.py
# Then run batch_sort.py or drop them into inbox while watcher runs
```

---

## How It Works

```
data/inbox/report.pdf
        │
        ▼
[classifier.py]
  .pdf → "documents"
        │
        ▼
[file_mover.py]
  Move to data/sorted/documents/20241201_123045_report.pdf
  Append row to logs/audit.csv
```

### Audit Log Format (`logs/audit.csv`)

| timestamp | original_name | extension | category | destination | status |
|-----------|--------------|-----------|----------|-------------|--------|
| 2024-12-01T12:30:45 | report.pdf | .pdf | documents | .../documents/20241201_123045_report.pdf | ok |

---

## File Categories

| Category | Extensions |
|----------|-----------|
| `documents` | `.pdf`, `.doc`, `.docx`, `.txt`, `.rtf` |
| `spreadsheets` | `.xls`, `.xlsx`, `.csv`, `.ods` |
| `images` | `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.svg` |
| `audio` | `.mp3`, `.wav`, `.flac`, `.aac` |
| `video` | `.mp4`, `.avi`, `.mkv`, `.mov` |
| `archives` | `.zip`, `.tar`, `.gz`, `.rar`, `.7z` |
| `code` | `.py`, `.js`, `.html`, `.css`, `.json`, `.yaml` |
| `other` | anything else |

---

## Extension Challenge

Try extending this lab:
1. Add a new file category (e.g., `presentations` for `.ppt`, `.pptx`)
2. Add a `--dry-run` flag to `batch_sort.py` that shows what would happen without moving files
3. Generate a summary report from `audit.csv` using `pandas`
