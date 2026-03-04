"""Thin facade that delegates to the configured LLM provider.

The public interface (ask_question / check_health) is unchanged so that
extractor.py and other callers require zero modifications.
"""

import logging

from app.services.providers import get_provider

logger = logging.getLogger(__name__)

try:
    _provider = get_provider()
except Exception as e:
    logger.error("Failed to initialize LLM provider: %s", e)
    _provider = None


async def ask_question(
    document_text: str, question: str, *, model: str = ""
) -> dict:
    """Send a question about a document to the active LLM provider."""
    if model:
        provider = get_provider(model_override=model)
        return await provider.ask_question(document_text, question)

    if _provider is None:
        return {"answer": "Error: LLM provider not configured", "confidence": 0.0}
    return await _provider.ask_question(document_text, question)


async def check_health() -> bool:
    """Check if the active LLM provider is reachable."""
    if _provider is None:
        return False
    return await _provider.check_health()
