# Serve Funding Deal Manager

## Deployment

### Modal (GPU + Web)
- **App name:** `serve-funding-deal-manager`
- **Deploy command:** `python3 -m modal deploy modal_app.py`
- The deploy rebuilds Docker images, downloads model weights, and updates all functions (web endpoint + GPU classes)
- Web endpoint: `https://timmayyyy--serve-funding-deal-manager-web.modal.run`
- Modal dashboard: `https://modal.com/apps/timmayyyy/main/deployed/serve-funding-deal-manager`
- After changing `modal_app.py`, always redeploy — git push alone does NOT deploy to Modal
- Image builds bake model weights in, so first deploy after a model change takes longer (~5 min)

### Models
- Small/fast: Qwen 3 8B (`Qwen/Qwen3-8B`) on L4 ($0.80/h, 24GB VRAM)
- Large/accurate: Qwen 3 32B AWQ (`Qwen/Qwen3-32B-AWQ`) on L40S ($1.95/h, 48GB VRAM)
- vLLM >=0.9.0 required for Qwen 3 support

## Project Structure
- `modal_app.py` — Modal app definition (GPU classes + web entrypoint)
- `app/` — FastAPI backend (mounted into Modal web function)
- `app/services/providers/` — LLM provider abstraction (modal_vllm, anthropic, openai, ollama)
- `frontend/` — Next.js frontend

## Key Conventions
- Model selector keys follow pattern `qwen-{size}` (e.g., `qwen-8b`, `qwen-32b`)
- Modal class names match model size (e.g., `Qwen8B`, `Qwen32B`)
- `_CLASS_MAP` in `modal_vllm.py` maps selector keys to Modal class names
- `MODAL_MODELS` set in `providers/__init__.py` must stay in sync with `_CLASS_MAP`
