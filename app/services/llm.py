"""Thin facade that delegates to the configured LLM provider.

The public interface (ask_question / check_health) is unchanged so that
extractor.py and other callers require zero modifications.
"""

from app.services.providers import get_provider

_provider = get_provider()


async def ask_question(document_text: str, question: str) -> dict:
    """Send a question about a document to the active LLM provider."""
    return await _provider.ask_question(document_text, question)


async def check_health() -> bool:
    """Check if the active LLM provider is reachable."""
    return await _provider.check_health()
