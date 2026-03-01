# Intelligent Automation Projects Repository

Welcome to the **Intelligent Automation Projects Repository**. This repository contains 10 hands-on labs that demonstrate the application of Intelligent Automation (IA) across various domains and use cases. Each lab is self-contained and showcases how AI, BPM, and RPA technologies integrate to streamline processes and drive business transformation.

## What is Intelligent Automation?

**Intelligent Automation (IA)** is the combination of multiple automation technologies — primarily **Artificial Intelligence (AI)**, **Business Process Management (BPM)**, and **Robotic Process Automation (RPA)** — to automate complex business processes and decision-making.

### Core Pillars

| Pillar | Description | Examples |
|--------|-------------|---------|
| **RPA** | Software bots handle repetitive, rule-based tasks | File management, web scraping, email handling |
| **AI** | Machine learning and NLP analyze data and generate insights | Sentiment analysis, image classification, chatbots |
| **BPM** | Workflows orchestrate and route tasks across systems | API-driven pipelines, approval processes, notifications |

---

## Labs Index

| # | Lab | Pillar | Key Technology | Difficulty |
|---|-----|--------|---------------|------------|
| 01 | [File & Folder Automation](./Lab-01-File-And-Folder-Automation/) | RPA | `watchdog`, `pathlib`, `shutil` | Beginner |
| 02 | [Web Scraping & Data Extraction](./Lab-02-Web-Scraping/) | RPA | `BeautifulSoup4`, `requests`, `pandas` | Beginner |
| 03 | [Email Automation](./Lab-03-Email-Automation/) | RPA | `smtplib`, `imaplib`, `schedule` | Beginner |
| 04 | [PDF & OCR Document Processing](./Lab-04-PDF-And-OCR-Processing/) | RPA + AI | `pdfplumber`, `pytesseract`, `Pillow` | Intermediate |
| 05 | [NLP Sentiment Analysis Pipeline](./Lab-05-NLP-Sentiment-Analysis/) | AI | `nltk`, `scikit-learn`, `matplotlib` | Intermediate |
| 06 | [ML Predictive Analytics Pipeline](./Lab-06-ML-Predictive-Pipeline/) | AI | `scikit-learn`, `pandas`, `joblib` | Intermediate |
| 07 | [API-Driven Process Automation](./Lab-07-API-Process-Automation/) | BPM | `FastAPI`, `httpx`, `schedule` | Intermediate |
| 08 | [Computer Vision & Image Processing](./Lab-08-Computer-Vision/) | AI | `OpenCV`, `Pillow`, `scikit-learn` | Intermediate |
| 09 | [Conversational Chatbot](./Lab-09-Conversational-Chatbot/) | AI | `nltk`, `Flask`, `transformers` | Intermediate |
| 10 | [End-to-End IA Pipeline](./Lab-10-End-To-End-IA-Pipeline/) | AI + BPM + RPA | Integrates Labs 2, 4, 5, 6, 7 | Advanced |

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    RPA Layer                            │
│   Lab 01: File Automation   Lab 02: Web Scraping        │
│   Lab 03: Email Automation  Lab 04: OCR / PDF           │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│                    AI Layer                             │
│   Lab 05: Sentiment Analysis  Lab 06: ML Pipeline       │
│   Lab 08: Computer Vision     Lab 09: Chatbot           │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│                    BPM Layer                            │
│              Lab 07: API Workflow Automation            │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│            Integration Layer (Lab 10)                   │
│      Scrape → Extract → Analyze → Predict → Notify      │
└─────────────────────────────────────────────────────────┘
```

---

## Getting Started

### Prerequisites

- Python 3.9+
- `pip` package manager
- Tesseract OCR (for Lab 04): `sudo apt install tesseract-ocr`
- OpenCV system dependencies (for Lab 08): `sudo apt install libgl1`

### Running a Lab

```bash
# 1. Navigate to a lab directory
cd Lab-01-File-And-Folder-Automation

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Follow the lab README
```

Each lab's `README.md` contains detailed setup instructions, explanations of key concepts, and step-by-step usage guides.

---

## Repository Structure

```
Intelligent-Automation/
├── README.md
├── .gitignore
├── Lab-01-File-And-Folder-Automation/
│   ├── README.md
│   ├── requirements.txt
│   ├── src/
│   └── data/
├── Lab-02-Web-Scraping/
│   ├── README.md
│   ├── requirements.txt
│   ├── src/
│   └── data/
...
└── Lab-10-End-To-End-IA-Pipeline/
    ├── README.md
    ├── requirements.txt
    ├── src/
    └── data/
```

---

## License

This repository is licensed under the [GNU General Public License v3.0](./LICENSE).
