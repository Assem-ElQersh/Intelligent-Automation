"""
Lab 05 — NLP Sentiment Analysis
Text preprocessing: tokenization, stopword removal, lemmatization.
"""

import re
import nltk

# Download required NLTK data (runs once, then cached)
for resource in ["stopwords", "wordnet", "punkt", "punkt_tab", "averaged_perceptron_tagger"]:
    try:
        nltk.data.find(f"tokenizers/{resource}")
    except LookupError:
        nltk.download(resource, quiet=True)

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

STOP_WORDS = set(stopwords.words("english"))
LEMMATIZER = WordNetLemmatizer()


def clean_text(text: str) -> str:
    """Lowercase, remove punctuation and numbers, strip whitespace."""
    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize(text: str) -> list[str]:
    return word_tokenize(text)


def remove_stopwords(tokens: list[str]) -> list[str]:
    return [t for t in tokens if t not in STOP_WORDS and len(t) > 2]


def lemmatize(tokens: list[str]) -> list[str]:
    return [LEMMATIZER.lemmatize(t) for t in tokens]


def preprocess(text: str) -> str:
    """Full preprocessing pipeline → returns a clean joined string."""
    text = clean_text(text)
    tokens = tokenize(text)
    tokens = remove_stopwords(tokens)
    tokens = lemmatize(tokens)
    return " ".join(tokens)
