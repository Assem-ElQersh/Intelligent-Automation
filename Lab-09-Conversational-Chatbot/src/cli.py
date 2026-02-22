"""
Lab 09 — Conversational Chatbot
CLI mode: chat with the bot in the terminal without running the web server.

Usage:
    python cli.py
"""

from chatbot import Chatbot


def main() -> None:
    print("=== Lab 09: Chatbot CLI ===")
    print("Type your message and press Enter. Type 'quit' to exit.\n")

    bot = Chatbot()

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if user_input.lower() in ("quit", "exit", "bye"):
            print("Bot: Goodbye! Have a great day!")
            break

        if not user_input:
            continue

        result = bot.respond(user_input)
        print(f"Bot: {result['response']}")
        print(f"     [intent={result['intent']} | confidence={result['confidence']:.0%}]\n")


if __name__ == "__main__":
    main()
