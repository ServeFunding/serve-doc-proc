from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ollama_base_url: str = "http://ollama:11434"
    ollama_model: str = "qwen2.5:7b"
    default_confidence_threshold: float = 0.7
    request_timeout: float = 120.0
    max_retries: int = 2
    max_upload_size_mb: int = 50

    model_config = {"env_prefix": "APP_"}


settings = Settings()
