"""Base protocol and shared helpers for LLM providers."""

import json
import logging
from typing import Protocol, runtime_checkable

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a document data extraction assistant. You will be given text extracted from a financial document and a specific question about that document.

Rules:
1. Answer the question based ONLY on the provided document text.
2. Return your answer as JSON with exactly two fields: "answer" and "confidence".
3. "answer" should be the extracted value as a concise string.
4. "confidence" should be a float between 0.0 and 1.0 indicating how clearly the information appears in the document.
   - 1.0 = the information is explicitly and clearly stated
   - 0.7-0.9 = the information is present but requires minor interpretation
   - 0.3-0.6 = the information is partially present or ambiguous
   - 0.0 = the information is not found in the document
5. If the information is not found, set "answer" to "Not found" and "confidence" to 0.0.

Respond with ONLY the JSON object, no other text."""


def build_user_message(document_text: str, question: str) -> str:
    """Build the user message for the LLM prompt."""
    return f"Document text:\n\n{document_text}\n\nQuestion: {question}"


def parse_llm_response(content: str) -> dict:
    """Parse an LLM response string into a standardized answer dict."""
    parsed = json.loads(content)
    return {
        "answer": str(parsed.get("answer", "Not found")),
        "confidence": float(parsed.get("confidence", 0.0)),
    }


@runtime_checkable
class LLMProvider(Protocol):
    """Protocol that all LLM providers must implement."""

    async def ask_question(self, document_text: str, question: str) -> dict: ...

    async def check_health(self) -> bool: ...
