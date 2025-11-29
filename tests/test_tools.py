"""Tests for the tools module."""

import pytest
from src.tools.example_tool import (
    CalculatorTool,
    CalculatorInput,
    CalculatorOutput,
    WebSearchTool,
    WebSearchInput,
    WebSearchOutput,
)


class TestCalculatorTool:
    """Tests for the CalculatorTool."""

    def test_addition(self) -> None:
        """Test addition operation."""
        tool = CalculatorTool()
        input_data = CalculatorInput(operation="add", a=5, b=3)
        result = tool.execute(input_data)

        assert isinstance(result, CalculatorOutput)
        assert result.result == 8
        assert result.operation == "add"

    def test_subtraction(self) -> None:
        """Test subtraction operation."""
        tool = CalculatorTool()
        input_data = CalculatorInput(operation="subtract", a=10, b=4)
        result = tool.execute(input_data)

        assert result.result == 6
        assert result.operation == "subtract"

    def test_multiplication(self) -> None:
        """Test multiplication operation."""
        tool = CalculatorTool()
        input_data = CalculatorInput(operation="multiply", a=6, b=7)
        result = tool.execute(input_data)

        assert result.result == 42
        assert result.operation == "multiply"

    def test_division(self) -> None:
        """Test division operation."""
        tool = CalculatorTool()
        input_data = CalculatorInput(operation="divide", a=20, b=4)
        result = tool.execute(input_data)

        assert result.result == 5
        assert result.operation == "divide"

    def test_division_by_zero(self) -> None:
        """Test that division by zero raises an error."""
        tool = CalculatorTool()
        input_data = CalculatorInput(operation="divide", a=10, b=0)

        with pytest.raises(ValueError, match="Division by zero"):
            tool.execute(input_data)

    def test_invalid_operation(self) -> None:
        """Test that invalid operations raise an error."""
        tool = CalculatorTool()
        input_data = CalculatorInput(operation="modulo", a=10, b=3)

        with pytest.raises(ValueError, match="Invalid operation"):
            tool.execute(input_data)

    def test_floating_point_numbers(self) -> None:
        """Test operations with floating point numbers."""
        tool = CalculatorTool()
        input_data = CalculatorInput(operation="multiply", a=3.5, b=2.0)
        result = tool.execute(input_data)

        assert result.result == 7.0


class TestWebSearchTool:
    """Tests for the WebSearchTool."""

    def test_basic_search(self) -> None:
        """Test basic web search."""
        tool = WebSearchTool()
        input_data = WebSearchInput(query="test query", max_results=5)
        result = tool.execute(input_data)

        assert isinstance(result, WebSearchOutput)
        assert result.query == "test query"
        assert len(result.results) > 0
        assert len(result.results) <= 5

    def test_max_results_limit(self) -> None:
        """Test that max_results is respected."""
        tool = WebSearchTool()
        input_data = WebSearchInput(query="test", max_results=2)
        result = tool.execute(input_data)

        assert len(result.results) <= 2

    def test_result_structure(self) -> None:
        """Test that results have the expected structure."""
        tool = WebSearchTool()
        input_data = WebSearchInput(query="test", max_results=1)
        result = tool.execute(input_data)

        assert len(result.results) > 0
        first_result = result.results[0]
        assert "title" in first_result
        assert "url" in first_result
        assert "snippet" in first_result

    def test_validation_max_results_min(self) -> None:
        """Test that max_results has a minimum value."""
        with pytest.raises(ValueError):
            WebSearchInput(query="test", max_results=0)

    def test_validation_max_results_max(self) -> None:
        """Test that max_results has a maximum value."""
        with pytest.raises(ValueError):
            WebSearchInput(query="test", max_results=11)
