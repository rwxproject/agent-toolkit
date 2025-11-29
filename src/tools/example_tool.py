"""Example tool implementations for the ADK agent."""

from typing import Any, Dict
from pydantic import BaseModel, Field
import logging

logger = logging.getLogger(__name__)


class CalculatorInput(BaseModel):
    """Input schema for the calculator tool."""

    operation: str = Field(description="The operation to perform: add, subtract, multiply, divide")
    a: float = Field(description="First number")
    b: float = Field(description="Second number")


class CalculatorOutput(BaseModel):
    """Output schema for the calculator tool."""

    result: float = Field(description="The result of the calculation")
    operation: str = Field(description="The operation performed")


class CalculatorTool:
    """
    A simple calculator tool that performs basic arithmetic operations.

    This demonstrates how to create a tool with:
    - Input validation using Pydantic
    - Error handling
    - Structured output
    """

    name = "calculator"
    description = "Performs basic arithmetic operations (add, subtract, multiply, divide)"

    @staticmethod
    def execute(input_data: CalculatorInput) -> CalculatorOutput:
        """
        Execute the calculator operation.

        Args:
            input_data: Calculator input parameters

        Returns:
            Calculator output with result

        Raises:
            ValueError: If operation is invalid or division by zero
        """
        logger.info(
            f"Executing calculator: {input_data.operation} {input_data.a} and {input_data.b}"
        )

        operations = {
            "add": lambda a, b: a + b,
            "subtract": lambda a, b: a - b,
            "multiply": lambda a, b: a * b,
            "divide": lambda a, b: a / b if b != 0 else None,
        }

        if input_data.operation not in operations:
            raise ValueError(
                f"Invalid operation: {input_data.operation}. "
                f"Must be one of: {', '.join(operations.keys())}"
            )

        result = operations[input_data.operation](input_data.a, input_data.b)

        if result is None:
            raise ValueError("Division by zero is not allowed")

        return CalculatorOutput(result=result, operation=input_data.operation)


class WebSearchInput(BaseModel):
    """Input schema for the web search tool."""

    query: str = Field(description="The search query")
    max_results: int = Field(default=5, ge=1, le=10, description="Maximum number of results")


class WebSearchOutput(BaseModel):
    """Output schema for the web search tool."""

    results: list = Field(description="List of search results")
    query: str = Field(description="The original query")


class WebSearchTool:
    """
    A web search tool that searches the internet.

    This is a placeholder implementation. In a real application,
    you would integrate with a search API like Google Custom Search,
    Bing Search API, or SerpAPI.
    """

    name = "web_search"
    description = "Searches the web for information"

    @staticmethod
    def execute(input_data: WebSearchInput) -> WebSearchOutput:
        """
        Execute a web search.

        Args:
            input_data: Search input parameters

        Returns:
            Search results

        Note:
            This is a placeholder implementation. Integrate with an actual
            search API for production use.
        """
        logger.info(f"Searching for: {input_data.query}")

        # Placeholder results
        # TODO: Integrate with actual search API
        results = [
            {
                "title": f"Result 1 for '{input_data.query}'",
                "url": "https://example.com/1",
                "snippet": "This is a placeholder search result.",
            },
            {
                "title": f"Result 2 for '{input_data.query}'",
                "url": "https://example.com/2",
                "snippet": "Another placeholder result.",
            },
        ]

        return WebSearchOutput(
            results=results[: input_data.max_results], query=input_data.query
        )
