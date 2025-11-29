"""Conversational agent example - multi-turn conversations."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import AppConfig
from src.agent import ADKAgent


def main() -> None:
    """Run a conversational agent example."""
    print("=== Conversational ADK Agent Example ===\n")

    # Load configuration
    try:
        config = AppConfig.from_env()
    except ValueError as e:
        print(f"Error: {e}")
        print("\nPlease copy .env.example to .env and set your GOOGLE_API_KEY")
        return

    # Create agent
    agent = ADKAgent(config)

    print("This example demonstrates multi-turn conversations.")
    print("The agent maintains context throughout the conversation.\n")

    # Simulate a multi-turn conversation
    conversation = [
        "Hi, I'm planning a trip to Japan.",
        "What's the best time to visit?",
        "What about Tokyo specifically?",
        "Thanks! Can you recommend some must-see places there?",
    ]

    print("=== Multi-turn Conversation ===\n")
    for i, message in enumerate(conversation, 1):
        print(f"User (turn {i}): {message}")
        response = agent.process(message)
        print(f"Agent: {response.message}\n")

    # Show conversation history
    print("=== Conversation History ===")
    history = agent.get_history()
    print(f"Total messages: {len(history)}")
    print(f"Turns: {len(history) // 2}\n")

    # Interactive mode
    print("=== Interactive Mode ===")
    print("Type your messages below (or 'quit' to exit, 'reset' to clear history)\n")

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() == "quit":
                print("Goodbye!")
                break

            if user_input.lower() == "reset":
                agent.reset()
                print("Conversation history cleared.\n")
                continue

            response = agent.process(user_input)
            print(f"Agent: {response.message}\n")

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()
