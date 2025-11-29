# Architecture Overview

## Introduction

This ADK starter kit is built on Google's Agent Development Kit (ADK), providing a foundation for creating AI agents with tool-calling capabilities.

## Core Components

### 1. Configuration Layer (`src/config.py`)

The configuration layer manages all application settings:

- **AppConfig**: Main configuration container
- **ModelConfig**: AI model parameters (temperature, top_p, etc.)
- **AgentConfig**: Agent-specific settings

Configuration is loaded from environment variables (`.env` file), allowing easy deployment across different environments.

### 2. Agent Core (`src/agent.py`)

The `ADKAgent` class is the heart of the system:

```
┌─────────────────────────────────────┐
│          ADKAgent                   │
├─────────────────────────────────────┤
│ - config: AppConfig                 │
│ - conversation_history: List[Msg]   │
│ - tools: Dict[str, Tool]            │
├─────────────────────────────────────┤
│ + register_tool(name, tool)         │
│ + process(input) -> Response        │
│ + reset()                           │
│ + get_history()                     │
└─────────────────────────────────────┘
```

**Key responsibilities:**
- Managing conversation context
- Coordinating tool execution
- Handling multi-turn interactions
- Maintaining state between requests

### 3. Tools Layer (`src/tools/`)

Tools extend the agent's capabilities:

```python
class Tool:
    name: str              # Unique identifier
    description: str       # What the tool does
    execute(input) -> output  # Core functionality
```

**Tool lifecycle:**
1. Registration with agent
2. Discovery by model
3. Execution when called
4. Result integration into response

### 4. Examples (`examples/`)

Three example implementations demonstrate different patterns:

- **simple_agent.py**: Single-turn interactions
- **multi_tool_agent.py**: Tool integration
- **conversational_agent.py**: Multi-turn conversations

## Request Flow

```
User Input
    ↓
┌─────────────────────┐
│  ADKAgent.process() │
└─────────────────────┘
    ↓
┌─────────────────────┐
│  Add to history     │
└─────────────────────┘
    ↓
┌─────────────────────┐
│  Call ADK API       │
└─────────────────────┘
    ↓
┌─────────────────────┐
│  Tool execution?    │───No──→ Return response
└─────────────────────┘
    ↓ Yes
┌─────────────────────┐
│  Execute tool(s)    │
└─────────────────────┘
    ↓
┌─────────────────────┐
│  Integrate results  │
└─────────────────────┘
    ↓
┌─────────────────────┐
│  Generate response  │
└─────────────────────┘
    ↓
Return to user
```

## Multi-turn Conversations

The agent maintains conversation history to enable context-aware interactions:

```
Turn 1: User → "I'm planning a trip"
        Agent → "Where are you planning to go?"
        [Context: trip planning]

Turn 2: User → "Japan"
        Agent → "Great choice! When are you planning to visit?"
        [Context: trip to Japan]

Turn 3: User → "What's the weather like?"
        Agent → "In Japan, weather varies by season..."
        [Context: trip to Japan, weather inquiry]
```

## Tool Integration

### Adding a New Tool

1. **Define input/output schemas** (Pydantic models)
2. **Implement the tool class** with `execute()` method
3. **Register with agent** using `agent.register_tool()`
4. **Document tool capabilities** in description

Example:

```python
class WeatherInput(BaseModel):
    location: str
    units: str = "celsius"

class WeatherTool:
    name = "weather"
    description = "Get current weather for a location"

    @staticmethod
    def execute(input: WeatherInput) -> WeatherOutput:
        # Implementation
        pass

# Register with agent
agent.register_tool("weather", WeatherTool())
```

## Error Handling

The starter kit implements error handling at multiple levels:

1. **Input validation**: Pydantic schemas validate all inputs
2. **Tool execution**: Try-catch blocks with meaningful errors
3. **API errors**: Handle rate limits, timeouts, etc.
4. **Configuration errors**: Fail fast with clear messages

## Security Considerations

- **API Keys**: Stored in environment variables, never committed
- **Input validation**: All user inputs validated before processing
- **Rate limiting**: Consider implementing for production use
- **Tool permissions**: Limit tool capabilities to prevent abuse

## Scalability

For production deployments, consider:

1. **State management**: External storage for conversation history
2. **Caching**: Cache frequent queries and tool results
3. **Load balancing**: Distribute requests across instances
4. **Monitoring**: Track usage, errors, and performance
5. **Async operations**: Use async/await for better concurrency

## Extending the Starter Kit

### Adding New Features

1. **Streaming responses**: Implement response streaming for better UX
2. **Multi-modal input**: Support images, documents, etc.
3. **Advanced tools**: Integrate with databases, APIs, etc.
4. **Custom prompts**: Implement prompt templates and chains
5. **Memory systems**: Add long-term memory capabilities

### Integration Points

- **Web frameworks**: FastAPI, Flask, Django
- **Messaging platforms**: Slack, Discord, Teams
- **Cloud platforms**: Google Cloud Run, AWS Lambda
- **Databases**: PostgreSQL, MongoDB, Redis

## Best Practices

1. **Type hints**: Use throughout for better IDE support
2. **Testing**: Write tests for all tools and critical paths
3. **Logging**: Comprehensive logging for debugging
4. **Documentation**: Keep docs updated with code changes
5. **Version control**: Tag releases and maintain changelog
6. **Code review**: Review all changes before merging
7. **Monitoring**: Track errors and performance metrics

## Next Steps

1. Replace placeholder ADK API calls with actual implementation
2. Integrate real search APIs (Google Custom Search, etc.)
3. Add more sophisticated tools
4. Implement proper error recovery
5. Add authentication and authorization
6. Deploy to production environment
