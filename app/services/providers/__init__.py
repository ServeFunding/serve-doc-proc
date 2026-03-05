"""LLM provider factory."""

from app.config import settings
from app.services.providers.base import LLMProvider

MODAL_MODELS = {"qwen-8b", "qwen-32b"}


def get_provider(model_override: str = "") -> LLMProvider:
    """Return an LLM provider instance based on config or model override."""
    if model_override and model_override in MODAL_MODELS:
        from app.services.providers.modal_vllm import ModalVLLMProvider

        return ModalVLLMProvider(model_override)

    if model_override:
        raise ValueError(f"Unknown model override: {model_override!r}")

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
