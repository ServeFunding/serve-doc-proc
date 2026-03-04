import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.extract import router as extract_router

app = FastAPI(
    title="AI Document Extraction Service",
    description="Extract structured data from funding/finance documents using AI",
    version="1.0.0",
)

allowed_origins = [
    "http://localhost:3000",
    "https://serve-doc-proc.vercel.app",
]
if extra_origin := os.getenv("APP_CORS_ORIGIN"):
    allowed_origins.append(extra_origin)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(extract_router)
