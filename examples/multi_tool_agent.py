"""Multi-tool agent example - agent with multiple tools."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import AppConfig
from src.agent import ADKAgent
from src.tools import CalculatorTool, WebSearchTool


def main() -> None:
    """Run a multi-tool agent example."""
    print("=== Multi-Tool ADK Agent Example ===\n")

    # Load configuration
    try:
        config = AppConfig.from_env()
    except ValueError as e:
        print(f"Error: {e}")
        print("\nPlease copy .env.example to .env and set your GOOGLE_API_KEY")
        return

    # Create agent
    agent = ADKAgent(config)

    # Register tools
    calculator = CalculatorTool()
    web_search = WebSearchTool()

    agent.register_tool(calculator.name, calculator)
    agent.register_tool(web_search.name, web_search)

    print(f"Registered tools: {', '.join(agent.tools.keys())}\n")

    # Demonstrate tool usage
    print("=== Calculator Tool Demo ===")
    from src.tools.example_tool import CalculatorInput

    calc_input = CalculatorInput(operation="multiply", a=15, b=7)
    result = calculator.execute(calc_input)
    print(f"15 × 7 = {result.result}\n")

    print("=== Web Search Tool Demo ===")
    from src.tools.example_tool import WebSearchInput

    search_input = WebSearchInput(query="Google ADK documentation", max_results=3)
    search_result = web_search.execute(search_input)
    print(f"Search query: {search_result.query}")
    print(f"Found {len(search_result.results)} results:")
    for i, result in enumerate(search_result.results, 1):
        print(f"  {i}. {result['title']}")
        print(f"     URL: {result['url']}")
        print(f"     {result['snippet']}\n")

    # Example agent query that might use tools
    print("=== Agent with Tools ===")
    queries = [
        "Calculate 123 times 456",
        "Search for information about artificial intelligence",
    ]

    for query in queries:
        print(f"Query: {query}")
        response = agent.process(query)
        print(f"Response: {response.message}\n")


if __name__ == "__main__":
    main()
