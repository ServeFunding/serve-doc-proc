from fastapi import FastAPI

from app.routes.extract import router as extract_router

app = FastAPI(
    title="AI Document Extraction Service",
    description="Extract structured data from funding/finance documents using AI",
    version="1.0.0",
)

app.include_router(extract_router)
