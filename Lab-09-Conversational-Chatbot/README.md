# Lab 09 — Conversational Chatbot

**Pillar:** AI / NLP  
**Difficulty:** Intermediate  
**Estimated Time:** 60–90 minutes

---

## Objective

Build a domain-specific chatbot that:
- Trains an **intent classifier** (TF-IDF + SVM) on a JSON intents file
- Classifies user messages and selects a matching response
- Handles low-confidence inputs with graceful fallback
- Exposes a **Flask web interface** with a modern chat UI
- Supports a CLI mode for terminal interaction

---

## Concepts Covered

| Concept | Description |
|---------|-------------|
| Intent recognition | Classifying user messages into predefined categories |
| TF-IDF + SVM | Feature extraction + classification pipeline |
| Confidence threshold | Fallback responses for uncertain predictions |
| Web API (Flask) | `/chat` endpoint returning JSON responses |
| Jinja2 templating | Rendered HTML chat interface |
| Training pipeline | JSON intents → trained model → saved to disk |

---

## Project Structure

```
Lab-09-Conversational-Chatbot/
├── README.md
├── requirements.txt
├── src/
│   ├── trainer.py   # Train intent classifier from intents.json
│   ├── chatbot.py   # Core prediction engine
│   ├── app.py       # Flask web app (/ and /chat endpoints)
│   └── cli.py       # Terminal chat mode
├── data/
│   └── intents.json # 11 intents with 100+ training patterns
├── templates/
│   └── chat.html    # Modern chat UI (vanilla HTML/CSS/JS)
└── output/
    └── chatbot_model.pkl
```

---

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Usage

### Step 1: Train the chatbot

```bash
cd src
python trainer.py
```

### Step 2a: Web Interface

```bash
python app.py
# Open http://localhost:5009
```

### Step 2b: CLI (terminal mode)

```bash
python cli.py
```

---

## How It Works

```
data/intents.json
  [{tag, patterns[], responses[]}, ...]
        │
        ▼ [trainer.py]
  Preprocess patterns (lowercase, lemmatize, remove stopwords)
  TF-IDF (1+2-grams, 3000 features) + SVC (linear kernel)
  → output/chatbot_model.pkl
        │
        ▼ [chatbot.py — at inference time]
  Preprocess user input
  Predict intent + confidence
  If confidence < 35% → fallback
  Else → pick random response for predicted intent
        │
        ▼ Flask /chat endpoint
  {"response": "...", "intent": "...", "confidence": 0.87}
```

---

## Intents

| Tag | Example Pattern | Response Topic |
|-----|----------------|----------------|
| `greeting` | "Hi there!" | Greet the user |
| `goodbye` | "Bye!" | Farewell |
| `thanks` | "Thank you" | Acknowledgement |
| `product_info` | "What products do you sell?" | Product catalog |
| `pricing` | "How much does it cost?" | Pricing info |
| `shipping` | "How long is delivery?" | Shipping details |
| `returns` | "What is your return policy?" | Return policy |
| `order_status` | "Where is my order?" | Order tracking |
| `support` | "I need help" | Support escalation |
| `hours` | "When are you open?" | Business hours |
| `bot_info` | "Are you a bot?" | Bot description |
| `fallback` | *(low confidence)* | Graceful fallback |

---

## Extension Challenge

1. Add a new intent by editing `data/intents.json` and retraining
2. Add a **conversation history** (context window) so the bot remembers previous turns
3. Swap the SVM for a **transformer** (e.g., `sentence-transformers`) for semantic similarity
