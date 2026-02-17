"""Anthropic Claude LLM provider."""

import logging

from app.config import settings
from app.services.providers.base import (
    SYSTEM_PROMPT,
    build_user_message,
    parse_llm_response,
)

logger = logging.getLogger(__name__)


class AnthropicProvider:
    """LLM provider using the Anthropic Claude API."""

    def __init__(self) -> None:
        import anthropic

        self._client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)

    async def ask_question(self, document_text: str, question: str) -> dict:
        """Send a question about a document to Claude and parse the JSON response."""
        import anthropic

        last_error: Exception | None = None
        for attempt in range(settings.max_retries + 1):
            try:
                message = await self._client.messages.create(
                    model=settings.effective_model,
                    max_tokens=1024,
                    system=SYSTEM_PROMPT,
                    messages=[
                        {
                            "role": "user",
                            "content": build_user_message(document_text, question),
                        }
                    ],
                    temperature=0.1,
                )
                content = message.content[0].text
                return parse_llm_response(content)
            except (anthropic.APIError, Exception) as e:
                last_error = e
                logger.warning(
                    "Anthropic request attempt %d failed: %s", attempt + 1, str(e)
                )

        logger.error("All Anthropic request attempts failed: %s", str(last_error))
        return {"answer": "Error: extraction failed", "confidence": 0.0}

    async def check_health(self) -> bool:
        """Check if the Anthropic API is reachable."""
        import anthropic

        try:
            await self._client.messages.create(
                model=settings.effective_model,
                max_tokens=10,
                messages=[{"role": "user", "content": "ping"}],
            )
            return True
        except anthropic.APIError:
            return False
