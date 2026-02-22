"""
Lab 09 — Conversational Chatbot
Flask web app serving the chat UI and /chat API endpoint.

Usage:
    # Train the model first:
    python trainer.py

    # Then start the web app:
    python app.py
    # Open http://localhost:5009
"""

from pathlib import Path
from flask import Flask, render_template, request, jsonify
from chatbot import Chatbot

TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"

app = Flask(__name__, template_folder=str(TEMPLATE_DIR))

chatbot = Chatbot()


@app.route("/")
def index():
    return render_template("chat.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    user_message = data.get("message", "").strip()
    result = chatbot.respond(user_message)
    return jsonify(result)


@app.route("/health")
def health():
    return jsonify({"status": "ok", "model": "loaded"})


if __name__ == "__main__":
    print("=== Lab 09: Conversational Chatbot ===")
    print("Open http://localhost:5009 in your browser\n")
    app.run(host="0.0.0.0", port=5009, debug=False)
