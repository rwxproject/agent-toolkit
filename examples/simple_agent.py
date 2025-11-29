"""Simple agent example - single-turn interactions."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import AppConfig
from src.agent import ADKAgent


def main() -> None:
    """Run a simple agent example."""
    print("=== Simple ADK Agent Example ===\n")

    # Load configuration
    try:
        config = AppConfig.from_env()
    except ValueError as e:
        print(f"Error: {e}")
        print("\nPlease copy .env.example to .env and set your GOOGLE_API_KEY")
        return

    # Create agent
    agent = ADKAgent(config)

    # Example queries
    queries = [
        "What is the capital of France?",
        "Explain quantum computing in simple terms.",
        "What are the benefits of exercise?",
    ]

    print("Running example queries:\n")
    for i, query in enumerate(queries, 1):
        print(f"Query {i}: {query}")
        response = agent.process(query)
        print(f"Response: {response.message}\n")

        # Reset conversation after each query for single-turn interaction
        agent.reset()


if __name__ == "__main__":
    main()
