"""Configuration management for the ADK agent."""

import os
from typing import Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class ModelConfig(BaseModel):
    """Configuration for the AI model."""

    name: str = Field(default="gemini-1.5-pro", description="Model name to use")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Sampling temperature")
    top_p: float = Field(default=0.95, ge=0.0, le=1.0, description="Top-p sampling parameter")
    top_k: int = Field(default=40, ge=1, description="Top-k sampling parameter")
    max_output_tokens: int = Field(
        default=2048, ge=1, le=8192, description="Maximum tokens to generate"
    )


class AgentConfig(BaseModel):
    """Configuration for the ADK agent."""

    name: str = Field(default="ADK Starter Agent", description="Agent name")
    debug: bool = Field(default=False, description="Enable debug mode")
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(default="json", description="Log format (json or text)")


class AppConfig(BaseModel):
    """Main application configuration."""

    api_key: str = Field(description="Google API key")
    model: ModelConfig = Field(default_factory=ModelConfig)
    agent: AgentConfig = Field(default_factory=AgentConfig)

    @classmethod
    def from_env(cls) -> "AppConfig":
        """Load configuration from environment variables."""
        api_key = os.getenv("GOOGLE_API_KEY", "")
        if not api_key:
            raise ValueError(
                "GOOGLE_API_KEY environment variable is required. "
                "Please set it in your .env file or environment."
            )

        model_config = ModelConfig(
            name=os.getenv("MODEL_NAME", "gemini-1.5-pro"),
            temperature=float(os.getenv("TEMPERATURE", "0.7")),
            top_p=float(os.getenv("TOP_P", "0.95")),
            top_k=int(os.getenv("TOP_K", "40")),
            max_output_tokens=int(os.getenv("MAX_OUTPUT_TOKENS", "2048")),
        )

        agent_config = AgentConfig(
            name=os.getenv("AGENT_NAME", "ADK Starter Agent"),
            debug=os.getenv("DEBUG", "false").lower() == "true",
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            log_format=os.getenv("LOG_FORMAT", "json"),
        )

        return cls(api_key=api_key, model=model_config, agent=agent_config)
