"""
Lab 09 — Conversational Chatbot
Core chatbot engine: predict intent, select response.
"""

import random
from pathlib import Path

import joblib
import numpy as np

MODEL_PATH = Path(__file__).resolve().parent.parent / "output" / "chatbot_model.pkl"
CONFIDENCE_THRESHOLD = 0.35


class Chatbot:
    def __init__(self) -> None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"No trained model at {MODEL_PATH}. Run 'python trainer.py' first."
            )
        data = joblib.load(MODEL_PATH)
        self.pipeline = data["pipeline"]
        self.label_encoder = data["label_encoder"]
        self.intents = data["intents"]
        self.preprocess = data["preprocess_fn"]
        self._response_map = {
            intent["tag"]: intent["responses"]
            for intent in self.intents["intents"]
        }

    def _get_fallback(self) -> str:
        return random.choice(self._response_map.get("fallback", ["I'm not sure how to help with that."]))

    def respond(self, user_input: str) -> dict:
        """
        Process user input and return a response dict.

        Returns:
            {
              "response": str,
              "intent": str,
              "confidence": float,
            }
        """
        if not user_input.strip():
            return {"response": "Please type something!", "intent": "empty", "confidence": 0.0}

        processed = self.preprocess(user_input)
        proba = self.pipeline.predict_proba([processed])[0]
        top_idx = int(np.argmax(proba))
        confidence = float(proba[top_idx])
        tag = self.label_encoder.inverse_transform([top_idx])[0]

        if confidence < CONFIDENCE_THRESHOLD:
            return {
                "response": self._get_fallback(),
                "intent": "fallback",
                "confidence": confidence,
            }

        responses = self._response_map.get(tag, [])
        response = random.choice(responses) if responses else self._get_fallback()

        return {
            "response": response,
            "intent": tag,
            "confidence": round(confidence, 3),
        }
