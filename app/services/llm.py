import json
import logging

import httpx

from app.config import settings

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


async def ask_question(document_text: str, question: str) -> dict:
    """Send a question about a document to Ollama and parse the JSON response."""
    url = f"{settings.ollama_base_url}/v1/chat/completions"
    payload = {
        "model": settings.ollama_model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Document text:\n\n{document_text}\n\nQuestion: {question}",
            },
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0.1,
        "stream": False,
    }

    last_error = None
    for attempt in range(settings.max_retries + 1):
        try:
            async with httpx.AsyncClient(
                timeout=settings.request_timeout
            ) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()

            data = response.json()
            content = data["choices"][0]["message"]["content"]
            parsed = json.loads(content)

            return {
                "answer": str(parsed.get("answer", "Not found")),
                "confidence": float(parsed.get("confidence", 0.0)),
            }
        except (httpx.HTTPError, json.JSONDecodeError, KeyError) as e:
            last_error = e
            logger.warning(
                "LLM request attempt %d failed: %s", attempt + 1, str(e)
            )

    logger.error("All LLM request attempts failed: %s", str(last_error))
    return {"answer": "Error: extraction failed", "confidence": 0.0}


async def check_ollama_health() -> bool:
    """Check if Ollama is reachable."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(settings.ollama_base_url)
            return response.status_code == 200
    except httpx.HTTPError:
        return False
