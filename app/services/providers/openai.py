"""OpenAI GPT LLM provider."""

import logging

from app.config import settings
from app.services.providers.base import (
    SYSTEM_PROMPT,
    build_user_message,
    parse_llm_response,
)

logger = logging.getLogger(__name__)


class OpenAIProvider:
    """LLM provider using the OpenAI API."""

    def __init__(self) -> None:
        import openai

        self._client = openai.AsyncOpenAI(api_key=settings.openai_api_key)

    async def ask_question(
        self, document_text: str, question: str, *, system_prompt: str = ""
    ) -> dict:
        """Send a question about a document to GPT and parse the JSON response."""
        import openai

        last_error: Exception | None = None
        for attempt in range(settings.max_retries + 1):
            try:
                response = await self._client.chat.completions.create(
                    model=settings.effective_model,
                    messages=[
                        {"role": "system", "content": system_prompt or SYSTEM_PROMPT},
                        {
                            "role": "user",
                            "content": build_user_message(document_text, question),
                        },
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.1,
                )
                content = response.choices[0].message.content
                return parse_llm_response(content)
            except (openai.APIError, Exception) as e:
                last_error = e
                logger.warning(
                    "OpenAI request attempt %d failed: %s", attempt + 1, str(e)
                )

        logger.error("All OpenAI request attempts failed: %s", str(last_error))
        return {"answer": "Error: extraction failed", "confidence": 0.0}

    async def check_health(self) -> bool:
        """Check if the OpenAI API is reachable."""
        import openai

        try:
            await self._client.models.list()
            return True
        except openai.APIError:
            return False
