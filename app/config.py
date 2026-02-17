from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    llm_provider: Literal["anthropic", "openai", "ollama"] = "anthropic"
    llm_model: str = ""
    anthropic_api_key: str = ""
    openai_api_key: str = ""
    ollama_base_url: str = "http://ollama:11434"
    default_confidence_threshold: float = 0.7
    request_timeout: float = 120.0
    max_retries: int = 2
    max_upload_size_mb: int = 50

    @property
    def effective_model(self) -> str:
        """Return the configured model or a sensible default for the active provider."""
        if self.llm_model:
            return self.llm_model
        defaults = {
            "anthropic": "claude-haiku-4-5-20251001",
            "openai": "gpt-4.1-mini",
            "ollama": "qwen2.5:7b",
        }
        return defaults[self.llm_provider]

    model_config = {"env_prefix": "APP_"}


settings = Settings()
