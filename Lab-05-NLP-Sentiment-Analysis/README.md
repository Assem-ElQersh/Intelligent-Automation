# Lab 05 — NLP Sentiment Analysis Pipeline

**Pillar:** AI / Natural Language Processing  
**Difficulty:** Intermediate  
**Estimated Time:** 45–60 minutes

---

## Objective

Build a complete NLP pipeline that:
- Preprocesses customer review text (tokenize, remove stopwords, lemmatize)
- Trains a TF-IDF + Logistic Regression classifier
- Evaluates performance with cross-validation and a classification report
- Generates visualizations: sentiment distribution, word clouds, confusion matrix
- Exports the trained model for reuse

---

## Concepts Covered

| Concept | Description |
|---------|-------------|
| Text preprocessing | Cleaning, tokenizing, stopword removal, lemmatization |
| TF-IDF | Term Frequency–Inverse Document Frequency vectorization |
| Classification | Logistic Regression for multi-class sentiment |
| Cross-validation | K-fold evaluation for robust performance estimates |
| Model persistence | Saving and loading models with `joblib` |
| Visualization | Distribution charts, word clouds, confusion matrix |

---

## Project Structure

```
Lab-05-NLP-Sentiment-Analysis/
├── README.md
├── requirements.txt
├── src/
│   ├── preprocessor.py   # Text cleaning pipeline (NLTK)
│   ├── trainer.py        # TF-IDF + LR training, evaluation, model save
│   ├── visualizer.py     # Charts: distribution, word clouds, confusion matrix
│   └── main.py           # Entry point
├── data/
│   └── reviews.csv       # 40 labeled customer reviews (pos/neg/neutral)
└── output/
    ├── sentiment_model.pkl
    ├── sentiment_distribution.png
    ├── wordcloud_positive.png
    ├── wordcloud_negative.png
    ├── wordcloud_neutral.png
    └── confusion_matrix.png
```

---

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

NLTK data (stopwords, wordnet, punkt) will be auto-downloaded on first run.

---

## Usage

### Train and visualize

```bash
cd src
python main.py
```

### Predict sentiment for a custom text

```bash
python main.py --predict "The product arrived broken and customer service was awful"
# → NEGATIVE

python main.py --predict "Absolutely love this, best purchase I've made this year!"
# → POSITIVE
```

---

## How It Works

```
data/reviews.csv
        │
        ▼ [preprocessor.py]
  lowercase → remove punctuation → tokenize
  → remove stopwords → lemmatize → rejoin
        │
        ▼ [trainer.py]
  TF-IDF (unigrams + bigrams, top 5000 features)
  → Logistic Regression (multinomial, C=1.0)
  → Train/test split + 5-fold cross-validation
  → output/sentiment_model.pkl
        │
        ▼ [visualizer.py]
  sentiment_distribution.png
  wordcloud_{positive,negative,neutral}.png
  confusion_matrix.png
```

---

## Dataset

40 synthetic customer reviews (balanced: 14 positive, 13 negative, 13 neutral).  
To use your own dataset, ensure your CSV has `review` and `sentiment` columns.

---

## Extension Challenge

1. Replace Logistic Regression with a **Random Forest** or **SVM** and compare accuracy
2. Add a **bigram analysis** to find the most common 2-word phrases per sentiment
3. Build a simple web interface with Flask to accept live review input and return predictions
