import time

from app.models.schemas import ExtractionResponse, ExtractionStats, QuestionResult
from app.services.llm import ask_question
from app.templates.funding import get_template


async def extract_from_document(
    document_text: str,
    template_name: str,
    threshold: float = 0.7,
    *,
    model: str = "",
) -> ExtractionResponse:
    """Run all template questions against document text and return results."""
    template = get_template(template_name)
    if template is None:
        raise ValueError(f"Unknown template: {template_name}")

    questions = template["questions"]
    results: dict[str, QuestionResult] = {}
    start_time = time.time()

    for field_key, question in questions.items():
        raw = await ask_question(document_text, question, model=model)
        results[field_key] = QuestionResult(
            answer=raw["answer"],
            confidence=raw["confidence"],
        )

    filtered_results: dict[str, str] = {
        key: result.answer
        for key, result in results.items()
        if result.confidence >= threshold
    }

    above = sum(1 for r in results.values() if r.confidence >= threshold)
    processing_time = time.time() - start_time

    return ExtractionResponse(
        template=template_name,
        threshold=threshold,
        model=model,
        results=results,
        filtered_results=filtered_results,
        stats=ExtractionStats(
            total_questions=len(questions),
            above_threshold=above,
            below_threshold=len(questions) - above,
            processing_time_seconds=round(processing_time, 2),
        ),
    )
