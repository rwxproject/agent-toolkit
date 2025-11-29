# ADK Starter Kit

A comprehensive starter kit for building AI agents with [Google's Agent Development Kit (ADK)](https://google.github.io/adk-docs/).

## Features

- **Ready-to-use agent implementation** with configuration management
- **Example tools** (calculator, web search) demonstrating tool integration
- **Multiple example patterns** (single-turn, multi-turn, tool usage)
- **Type-safe** with Pydantic models and Python type hints
- **Well-tested** with pytest test suite
- **Production-ready** project structure with proper error handling
- **Extensible** architecture for adding custom tools and capabilities

## Quick Start

### Prerequisites

- Python 3.10 or higher
- Google API key (for Google AI/Gemini models)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd agent-toolkit
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e .
```

4. Set up environment variables:
```bash
cp .env.example .env
```

Edit `.env` and add your Google API key:
```env
GOOGLE_API_KEY=your_api_key_here
```

### Running Examples

#### Simple Agent (Single-turn)
```bash
python examples/simple_agent.py
```

#### Multi-tool Agent
```bash
python examples/multi_tool_agent.py
```

#### Conversational Agent (Interactive)
```bash
python examples/conversational_agent.py
```

## Project Structure

```
agent-toolkit/
├── src/                      # Source code
│   ├── __init__.py
│   ├── agent.py             # Main agent implementation
│   ├── config.py            # Configuration management
│   ├── tools/               # Custom tools
│   │   ├── __init__.py
│   │   └── example_tool.py  # Calculator and web search tools
│   └── prompts/             # System prompts
│       └── system_prompt.txt
├── examples/                # Example implementations
│   ├── simple_agent.py      # Single-turn interactions
│   ├── multi_tool_agent.py  # Tool usage examples
│   └── conversational_agent.py  # Multi-turn conversations
├── tests/                   # Test suite
│   ├── __init__.py
│   ├── test_agent.py
│   └── test_tools.py
├── docs/                    # Documentation
│   └── architecture.md      # Architecture overview
├── pyproject.toml           # Project configuration and dependencies
├── .env.example             # Environment variable template
├── .gitignore
└── README.md
```

## Core Components

### Agent (`src/agent.py`)

The `ADKAgent` class provides the main agent functionality:

```python
from src.config import AppConfig
from src.agent import ADKAgent

# Load configuration
config = AppConfig.from_env()

# Create agent
agent = ADKAgent(config)

# Process input
response = agent.process("What is the capital of France?")
print(response.message)
```

### Configuration (`src/config.py`)

Configuration is managed through environment variables:

```python
from src.config import AppConfig

# Load from environment
config = AppConfig.from_env()

# Access settings
print(config.model.name)        # gemini-1.5-pro
print(config.model.temperature)  # 0.7
print(config.agent.name)        # ADK Starter Agent
```

### Tools (`src/tools/`)

Tools extend agent capabilities. Example calculator tool:

```python
from src.tools import CalculatorTool
from src.tools.example_tool import CalculatorInput

tool = CalculatorTool()
result = tool.execute(CalculatorInput(
    operation="multiply",
    a=15,
    b=7
))
print(result.result)  # 105
```

## Creating Custom Tools

1. Define input/output schemas using Pydantic:

```python
from pydantic import BaseModel, Field

class MyToolInput(BaseModel):
    query: str = Field(description="The query to process")

class MyToolOutput(BaseModel):
    result: str = Field(description="The result")
```

2. Implement the tool class:

```python
class MyTool:
    name = "my_tool"
    description = "Description of what the tool does"

    @staticmethod
    def execute(input_data: MyToolInput) -> MyToolOutput:
        # Your implementation here
        result = process(input_data.query)
        return MyToolOutput(result=result)
```

3. Register with the agent:

```python
agent.register_tool("my_tool", MyTool())
```

## Configuration Options

Environment variables (set in `.env`):

| Variable | Description | Default |
|----------|-------------|---------|
| `GOOGLE_API_KEY` | Google API key (required) | - |
| `MODEL_NAME` | Model to use | `gemini-1.5-pro` |
| `TEMPERATURE` | Sampling temperature (0.0-2.0) | `0.7` |
| `TOP_P` | Top-p sampling (0.0-1.0) | `0.95` |
| `TOP_K` | Top-k sampling | `40` |
| `MAX_OUTPUT_TOKENS` | Max tokens to generate | `2048` |
| `AGENT_NAME` | Name for the agent | `ADK Starter Agent` |
| `DEBUG` | Enable debug mode | `false` |
| `LOG_LEVEL` | Logging level | `INFO` |

## Testing

Run the test suite:

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_agent.py
```

## Development

### Code Quality

The project uses several tools for code quality:

```bash
# Format code
black src/ tests/ examples/

# Lint
ruff check src/ tests/ examples/

# Type checking
mypy src/
```

### Adding Dependencies

Add to `pyproject.toml` under `dependencies` or `dev` (for development dependencies), then:

```bash
pip install -e ".[dev]"
```

## Architecture

For detailed architecture documentation, see [docs/architecture.md](docs/architecture.md).

Key concepts:

- **Configuration layer**: Environment-based settings
- **Agent core**: Main agent logic and conversation management
- **Tools layer**: Extensible tool system
- **Type safety**: Pydantic models for validation
- **Error handling**: Comprehensive error handling throughout

## Examples

### Single-turn Interaction

```python
from src.config import AppConfig
from src.agent import ADKAgent

config = AppConfig.from_env()
agent = ADKAgent(config)

response = agent.process("What is 15 times 7?")
print(response.message)
```

### Multi-turn Conversation

```python
agent = ADKAgent(config)

# Turn 1
response1 = agent.process("I'm planning a trip to Japan")
print(response1.message)

# Turn 2 (agent remembers context)
response2 = agent.process("What's the best time to visit?")
print(response2.message)

# View conversation history
history = agent.get_history()
print(f"Total messages: {len(history)}")
```

### Using Tools

```python
from src.tools import CalculatorTool

agent = ADKAgent(config)
calculator = CalculatorTool()
agent.register_tool(calculator.name, calculator)

# Agent can now use the calculator tool
response = agent.process("Calculate 123 times 456")
print(response.message)
```

## Deployment

### Environment Setup

For production deployment:

1. Set environment variables securely (use secrets management)
2. Configure appropriate logging
3. Set up monitoring and error tracking
4. Implement rate limiting
5. Use production-grade API keys

### Docker (Optional)

Create a `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN pip install -e .

CMD ["python", "examples/simple_agent.py"]
```

## Troubleshooting

### API Key Issues

```
Error: GOOGLE_API_KEY environment variable is required
```

**Solution**: Ensure `.env` file exists with valid `GOOGLE_API_KEY`

### Import Errors

```
ModuleNotFoundError: No module named 'src'
```

**Solution**: Install the package: `pip install -e .`

### Tool Execution Errors

Check:
- Input data matches the tool's input schema
- Tool is properly registered with the agent
- Required dependencies are installed

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run tests and linting
6. Submit a pull request

## Resources

- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Google AI Python SDK](https://github.com/google/generative-ai-python)

## License

This starter kit is provided as-is for educational and development purposes.

## Next Steps

1. **Replace placeholder code**: Update `src/agent.py` with actual ADK API calls
2. **Add real tools**: Integrate with real APIs (Google Search, weather, etc.)
3. **Customize prompts**: Modify system prompts for your use case
4. **Add authentication**: Implement user authentication if needed
5. **Deploy**: Deploy to your preferred platform (Google Cloud Run, AWS, etc.)

## Support

For issues and questions:
- Check the [documentation](docs/architecture.md)
- Review the [examples](examples/)
- Open an issue on GitHub

---

Built with [Google Agent Development Kit (ADK)](https://google.github.io/adk-docs/)
