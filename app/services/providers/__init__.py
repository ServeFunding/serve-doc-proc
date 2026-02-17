"""LLM provider factory."""

from app.config import settings
from app.services.providers.base import LLMProvider


def get_provider() -> LLMProvider:
    """Return an LLM provider instance based on the current configuration."""
    provider = settings.llm_provider

    if provider == "anthropic":
        from app.services.providers.anthropic import AnthropicProvider

        return AnthropicProvider()

    if provider == "openai":
        from app.services.providers.openai import OpenAIProvider

        return OpenAIProvider()

    if provider == "ollama":
        from app.services.providers.ollama import OllamaProvider

        return OllamaProvider()

    raise ValueError(f"Unknown LLM provider: {provider!r}")
