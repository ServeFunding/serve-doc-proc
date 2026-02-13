# AI Document Extraction Service

Self-hosted API that processes funding/finance documents (merchant applications, bank statements), asks predefined questions against them using a local LLM, and returns answers with confidence scores.

## Architecture

- **FastAPI** — Receives document uploads, runs OCR, orchestrates LLM Q&A
- **Ollama** — Runs Qwen 2.5 7B locally for document question-answering
- **Tesseract** — OCR for scanned PDFs and images
- **PyMuPDF** — Native PDF text extraction (falls back to OCR for scanned pages)

## API Endpoints

### `POST /extract`

Upload a document and extract structured data.

**Form fields:**
- `file` — PDF, PNG, JPEG, TIFF, or BMP document
- `template` — Template name (`merchant_application` or `bank_statement`)
- `threshold` — Confidence threshold 0.0-1.0 (default: 0.7)

**Response:**
```json
{
  "template": "merchant_application",
  "threshold": 0.7,
  "results": {
    "business_name": {"answer": "ABC Corp", "confidence": 0.95},
    "owner_name": {"answer": "John Smith", "confidence": 0.88}
  },
  "filtered_results": {
    "business_name": "ABC Corp",
    "owner_name": "John Smith"
  },
  "stats": {
    "total_questions": 12,
    "above_threshold": 10,
    "below_threshold": 2,
    "processing_time_seconds": 45.2
  }
}
```

### `GET /templates`

Returns available templates and their questions.

### `GET /health`

Health check — verifies Ollama connectivity.

## Local Development

```bash
docker-compose up
```

This starts both services:
- **Ollama** on port 11434 (auto-pulls Qwen 2.5 7B on first start)
- **FastAPI** on port 8000

Test it:
```bash
# Health check
curl http://localhost:8000/health

# List templates
curl http://localhost:8000/templates

# Extract from a document
curl -X POST http://localhost:8000/extract \
  -F "file=@document.pdf" \
  -F "template=merchant_application" \
  -F "threshold=0.7"
```

## Railway Deployment

This project uses two Railway services:

1. **Ollama** — Use the official Ollama Railway template. Set it to pull `qwen2.5:7b`.
2. **FastAPI** — Deploy this repo. Set environment variable:
   - `APP_OLLAMA_BASE_URL` = internal URL of your Ollama service (e.g. `http://ollama.railway.internal:11434`)

## Configuration

Environment variables (all prefixed with `APP_`):

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_OLLAMA_BASE_URL` | `http://ollama:11434` | Ollama service URL |
| `APP_OLLAMA_MODEL` | `qwen2.5:7b` | Model to use |
| `APP_DEFAULT_CONFIDENCE_THRESHOLD` | `0.7` | Default confidence filter |
| `APP_REQUEST_TIMEOUT` | `120.0` | LLM request timeout (seconds) |
| `APP_MAX_RETRIES` | `2` | LLM request retry count |
| `APP_MAX_UPLOAD_SIZE_MB` | `50` | Max upload file size |
