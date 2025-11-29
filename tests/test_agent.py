"""Tests for the agent module."""

import pytest
from src.config import AppConfig, ModelConfig, AgentConfig
from src.agent import ADKAgent, Message, AgentResponse


@pytest.fixture
def test_config() -> AppConfig:
    """Create a test configuration."""
    return AppConfig(
        api_key="test_api_key",
        model=ModelConfig(name="gemini-1.5-pro", temperature=0.7),
        agent=AgentConfig(name="Test Agent", debug=True),
    )


@pytest.fixture
def agent(test_config: AppConfig) -> ADKAgent:
    """Create a test agent."""
    return ADKAgent(test_config)


def test_agent_initialization(agent: ADKAgent, test_config: AppConfig) -> None:
    """Test that the agent initializes correctly."""
    assert agent.config == test_config
    assert len(agent.conversation_history) == 0
    assert len(agent.tools) == 0


def test_register_tool(agent: ADKAgent) -> None:
    """Test tool registration."""
    mock_tool = {"name": "test_tool", "description": "A test tool"}
    agent.register_tool("test_tool", mock_tool)

    assert "test_tool" in agent.tools
    assert agent.tools["test_tool"] == mock_tool


def test_process_message(agent: ADKAgent) -> None:
    """Test processing a message."""
    response = agent.process("Hello, agent!")

    assert isinstance(response, AgentResponse)
    assert len(response.message) > 0
    assert len(agent.conversation_history) == 2  # User + assistant message


def test_conversation_history(agent: ADKAgent) -> None:
    """Test conversation history management."""
    agent.process("First message")
    agent.process("Second message")

    history = agent.get_history()
    assert len(history) == 4  # 2 user + 2 assistant messages
    assert history[0].role == "user"
    assert history[1].role == "assistant"


def test_reset_conversation(agent: ADKAgent) -> None:
    """Test resetting the conversation."""
    agent.process("Test message")
    assert len(agent.conversation_history) > 0

    agent.reset()
    assert len(agent.conversation_history) == 0


def test_message_model() -> None:
    """Test the Message model."""
    message = Message(role="user", content="Hello")
    assert message.role == "user"
    assert message.content == "Hello"


def test_agent_response_model() -> None:
    """Test the AgentResponse model."""
    response = AgentResponse(
        message="Test response", tool_calls=None, metadata={"key": "value"}
    )
    assert response.message == "Test response"
    assert response.tool_calls is None
    assert response.metadata == {"key": "value"}
