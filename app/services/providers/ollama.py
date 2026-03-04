"""Ollama (self-hosted) LLM provider."""

import json
import logging

import httpx

from app.config import settings
from app.services.providers.base import (
    SYSTEM_PROMPT,
    build_user_message,
    parse_llm_response,
)

logger = logging.getLogger(__name__)


class OllamaProvider:
    """LLM provider using a local Ollama instance via its OpenAI-compatible API."""

    async def ask_question(
        self, document_text: str, question: str, *, system_prompt: str = ""
    ) -> dict:
        """Send a question about a document to Ollama and parse the JSON response."""
        url = f"{settings.ollama_base_url}/v1/chat/completions"
        payload = {
            "model": settings.effective_model,
            "messages": [
                {"role": "system", "content": system_prompt or SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": build_user_message(document_text, question),
                },
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.1,
            "stream": False,
        }

        last_error: Exception | None = None
        for attempt in range(settings.max_retries + 1):
            try:
                async with httpx.AsyncClient(
                    timeout=settings.request_timeout
                ) as client:
                    response = await client.post(url, json=payload)
                    response.raise_for_status()

                data = response.json()
                content = data["choices"][0]["message"]["content"]
                return parse_llm_response(content)
            except (httpx.HTTPError, json.JSONDecodeError, KeyError) as e:
                last_error = e
                logger.warning(
                    "Ollama request attempt %d failed: %s", attempt + 1, str(e)
                )

        logger.error("All Ollama request attempts failed: %s", str(last_error))
        return {"answer": "Error: extraction failed", "confidence": 0.0}

    async def check_health(self) -> bool:
        """Check if Ollama is reachable."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(settings.ollama_base_url)
                return response.status_code == 200
        except httpx.HTTPError:
            return False
