"""LLM provider that calls vLLM GPU classes deployed on Modal."""

import logging

import modal

from app.services.providers.base import (
    SYSTEM_PROMPT,
    build_user_message,
    parse_llm_response,
)

logger = logging.getLogger(__name__)

_CLASS_MAP = {
    "qwen-8b": "Qwen8B",
    "qwen-32b": "Qwen32B",
}


class ModalVLLMProvider:
    """Routes requests to a Modal GPU class running vLLM."""

    def __init__(self, model_name: str) -> None:
        class_name = _CLASS_MAP[model_name]
        self._cls = modal.Cls.from_name(
            "serve-funding-deal-manager", class_name
        )
        self._model_name = model_name

    async def ask_question(
        self, document_text: str, question: str, *, system_prompt: str = ""
    ) -> dict:
        user_message = build_user_message(document_text, question)
        try:
            result = self._cls().generate.remote(system_prompt or SYSTEM_PROMPT, user_message)
            return parse_llm_response(result)
        except Exception as e:
            logger.error("Modal vLLM error (%s): %s", self._model_name, e)
            return {"answer": f"Error: {e}", "confidence": 0.0}

    async def check_health(self) -> bool:
        try:
            self._cls().generate.remote(
                "You are a test.", "Reply with the word 'ok'."
            )
            return True
        except Exception:
            return False
