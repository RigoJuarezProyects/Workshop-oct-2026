#!/usr/bin/env python3
"""
chat.py - A minimal command-line chat client for local LLMs running in Ollama.

Workshop script: lets you pick between two small local models (Llama 3.2 and
Qwen 2.5), type messages, and see streamed responses. Type 'switch' to change
models, or 'exit' / 'quit' (or Ctrl+C) to leave.

Prerequisites:
    1. Ollama installed and running (https://ollama.com/download)
    2. Both models pulled:
         ollama pull llama3.2
         ollama pull qwen2.5
    3. Python dependencies installed:
         pip install -r requirements.txt
"""

import sys

import ollama

# The two small models used in this workshop (2-4 GB range).
MODELS = {
    "1": "llama3.2",
    "2": "qwen2.5",
}


def choose_model() -> str:
    """Ask the user which model to chat with and return its Ollama tag."""
    print("\nWhich model would you like to talk to?")
    print("  1) llama3.2  (Meta, ~2.0 GB)")
    print("  2) qwen2.5   (Alibaba, ~1.9 GB)")

    while True:
        choice = input("Enter 1 or 2: ").strip()
        if choice in MODELS:
            return MODELS[choice]
        print("Sorry, I didn't understand that. Please type 1 or 2.")


def chat_loop(model: str) -> str | None:
    """
    Run the chat loop for the given model.

    Returns "switch" if the user wants to change models, or None if the
    user wants to exit the program entirely.
    """
    print(f"\nNow chatting with '{model}'. Type 'switch' to change models,")
    print("or 'exit' to quit.\n")

    # `messages` keeps the running conversation so the model has context
    # from earlier turns (this is what makes it a "chat" and not just a
    # one-off question/answer).
    messages: list[dict[str, str]] = []

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting. Bye!")
            return None

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit"):
            print("Bye!")
            return None

        if user_input.lower() == "switch":
            return "switch"

        messages.append({"role": "user", "content": user_input})

        print(f"{model}: ", end="", flush=True)
        reply_parts = []
        try:
            # stream=True lets us print each chunk of the response as it
            # arrives, instead of waiting for the whole answer at once.
            stream = ollama.chat(model=model, messages=messages, stream=True)
            for chunk in stream:
                text = chunk["message"]["content"]
                print(text, end="", flush=True)
                reply_parts.append(text)
        except ollama.ResponseError as e:
            print(f"\n[Error talking to Ollama: {e.error}]")
            if e.status_code == 404:
                print(f"It looks like '{model}' isn't pulled yet. Run:")
                print(f"  ollama pull {model}")
            # Drop the last user message since we didn't get a reply for it.
            messages.pop()
            continue
        except Exception as e:  # noqa: BLE001 - workshop script, keep it simple
            print(f"\n[Unexpected error: {e}]")
            messages.pop()
            continue

        print()  # newline after the streamed reply
        messages.append({"role": "assistant", "content": "".join(reply_parts)})


def main() -> None:
    print("=" * 50)
    print(" Local LLM Workshop - chat.py")
    print("=" * 50)
    print("Make sure Ollama is running and you've pulled both models:")
    print("  ollama pull llama3.2")
    print("  ollama pull qwen2.5")

    model = choose_model()
    while True:
        result = chat_loop(model)
        if result == "switch":
            model = choose_model()
            continue
        break

    sys.exit(0)


if __name__ == "__main__":
    main()
