import json
import logging
import time

from app.models.schemas import (
    EntityResult,
    ExtractionResponse,
    ExtractionStats,
    QuestionResult,
)
from app.services.llm import ask_question
from app.services.providers.base import (
    ENTITY_DETECTION_PROMPT,
    MULTI_ENTITY_SYSTEM_PROMPT,
)
from app.templates.funding import get_template

logger = logging.getLogger(__name__)


async def _detect_entities(document_text: str, *, model: str = "") -> list[str]:
    """Ask the LLM to identify distinct entities/products in the document."""
    raw = await ask_question(
        document_text,
        "List all distinct products, loan programs, or entities described in this document as a JSON array of short names.",
        model=model,
        system_prompt=ENTITY_DETECTION_PROMPT,
    )
    answer = raw.get("answer", "[]")
    try:
        entities = json.loads(answer)
        if isinstance(entities, list) and all(isinstance(e, str) for e in entities):
            return entities
    except (json.JSONDecodeError, TypeError):
        pass
    logger.warning("Entity detection returned unexpected format: %s", answer)
    return [answer] if answer and answer != "Not found" else []


async def _extract_single(
    document_text: str,
    questions: dict[str, str],
    threshold: float,
    *,
    model: str = "",
) -> tuple[dict[str, QuestionResult], dict[str, str]]:
    """Extract answers for all questions (single-entity mode)."""
    results: dict[str, QuestionResult] = {}
    for field_key, question in questions.items():
        raw = await ask_question(document_text, question, model=model)
        results[field_key] = QuestionResult(
            answer=raw["answer"],
            confidence=raw["confidence"],
        )

    filtered = {
        key: r.answer for key, r in results.items() if r.confidence >= threshold
    }
    return results, filtered


async def _extract_for_entity(
    document_text: str,
    entity_name: str,
    questions: dict[str, str],
    threshold: float,
    *,
    model: str = "",
) -> EntityResult:
    """Extract answers for one entity using the multi-entity system prompt."""
    results: dict[str, QuestionResult] = {}
    for field_key, question in questions.items():
        scoped_question = f"For '{entity_name}': {question}"
        raw = await ask_question(
            document_text,
            scoped_question,
            model=model,
            system_prompt=MULTI_ENTITY_SYSTEM_PROMPT,
        )
        results[field_key] = QuestionResult(
            answer=raw["answer"],
            confidence=raw["confidence"],
        )

    filtered = {
        key: r.answer for key, r in results.items() if r.confidence >= threshold
    }
    return EntityResult(name=entity_name, results=results, filtered_results=filtered)


async def extract_from_document(
    document_text: str,
    template_name: str,
    threshold: float = 0.7,
    *,
    model: str = "",
    multi_entity: bool = False,
) -> ExtractionResponse:
    """Run all template questions against document text and return results."""
    template = get_template(template_name)
    if template is None:
        raise ValueError(f"Unknown template: {template_name}")

    questions = template["questions"]
    start_time = time.time()
    entities: list[EntityResult] | None = None

    if multi_entity:
        entity_names = await _detect_entities(document_text, model=model)
        if len(entity_names) > 1:
            entity_results = []
            for name in entity_names:
                er = await _extract_for_entity(
                    document_text, name, questions, threshold, model=model
                )
                entity_results.append(er)
            entities = entity_results

            # Aggregate: use first entity as top-level results for backwards compat
            all_results = entities[0].results
            all_filtered = entities[0].filtered_results
        else:
            # Single entity detected — fall back to normal extraction
            all_results, all_filtered = await _extract_single(
                document_text, questions, threshold, model=model
            )
    else:
        all_results, all_filtered = await _extract_single(
            document_text, questions, threshold, model=model
        )

    above = sum(1 for r in all_results.values() if r.confidence >= threshold)
    processing_time = time.time() - start_time

    return ExtractionResponse(
        template=template_name,
        threshold=threshold,
        model=model,
        results=all_results,
        filtered_results=all_filtered,
        stats=ExtractionStats(
            total_questions=len(questions),
            above_threshold=above,
            below_threshold=len(questions) - above,
            processing_time_seconds=round(processing_time, 2),
        ),
        entities=entities,
    )
