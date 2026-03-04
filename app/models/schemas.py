from typing import List, Optional

from pydantic import BaseModel, Field


class QuestionResult(BaseModel):
    answer: str
    confidence: float = Field(ge=0.0, le=1.0)


class ExtractionStats(BaseModel):
    total_questions: int
    above_threshold: int
    below_threshold: int
    processing_time_seconds: float


class ExtractionResponse(BaseModel):
    template: str
    threshold: float
    model: str = ""
    results: dict[str, QuestionResult]
    filtered_results: dict[str, str]
    stats: ExtractionStats
    entities: Optional[List["EntityResult"]] = None


class TemplateInfo(BaseModel):
    name: str
    description: str
    questions: dict[str, str]


class TemplateListResponse(BaseModel):
    templates: list[TemplateInfo]


class TemplateUpdateRequest(BaseModel):
    questions: dict[str, str]


class EntityResult(BaseModel):
    name: str
    results: dict[str, QuestionResult]
    filtered_results: dict[str, str]


class HealthResponse(BaseModel):
    status: str
    provider: str
    provider_connected: bool
    model: str
