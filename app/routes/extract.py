from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.config import settings
from app.models.schemas import (
    ExtractionResponse,
    HealthResponse,
    TemplateInfo,
    TemplateListResponse,
)
from app.services.extractor import extract_from_document
from app.services.llm import check_health
from app.services.ocr import extract_text
from app.templates.funding import get_template, list_templates

router = APIRouter()

ALLOWED_CONTENT_TYPES = {
    "application/pdf",
    "image/png",
    "image/jpeg",
    "image/tiff",
    "image/bmp",
}

_bearer = HTTPBearer()


async def verify_api_key(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer),
) -> str:
    """Validate the Bearer token against the configured API key."""
    if not settings.api_key:
        raise HTTPException(
            status_code=500, detail="Server API key not configured"
        )
    if credentials.credentials != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return credentials.credentials


@router.post("/extract", response_model=ExtractionResponse)
async def extract_document(
    file: UploadFile = File(...),
    template: str = Form("merchant_application"),
    threshold: float = Form(0.7),
    model: str = Form(""),
    _key: str = Depends(verify_api_key),
):
    """Upload a document and extract structured data using a question template."""
    if get_template(template) is None:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown template: {template}. Use GET /templates to list available templates.",
        )

    if threshold < 0.0 or threshold > 1.0:
        raise HTTPException(
            status_code=400, detail="Threshold must be between 0.0 and 1.0"
        )

    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file.content_type}. Accepted: PDF, PNG, JPEG, TIFF, BMP",
        )

    file_bytes = await file.read()
    max_bytes = settings.max_upload_size_mb * 1024 * 1024
    if len(file_bytes) > max_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {settings.max_upload_size_mb}MB",
        )

    try:
        document_text = extract_text(file_bytes, file.content_type)
    except Exception as e:
        raise HTTPException(
            status_code=422, detail=f"Failed to extract text from document: {str(e)}"
        )

    if not document_text.strip():
        raise HTTPException(
            status_code=422,
            detail="No text could be extracted from the document. The file may be empty or unreadable.",
        )

    result = await extract_from_document(
        document_text, template, threshold, model=model
    )
    return result


@router.get("/templates", response_model=TemplateListResponse)
async def get_templates():
    """List available document templates and their questions."""
    templates = list_templates()
    return TemplateListResponse(
        templates=[
            TemplateInfo(
                name=name,
                description=info["description"],
                questions=info["questions"],
            )
            for name, info in templates.items()
        ]
    )


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Check service health and LLM provider connectivity."""
    connected = await check_health()
    return HealthResponse(
        status="ok" if connected else "degraded",
        provider=settings.llm_provider,
        provider_connected=connected,
        model=settings.effective_model,
    )
