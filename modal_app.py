import modal

app = modal.App("serve-funding-deal-manager")

# Shared volume for caching model weights across cold starts
model_cache = modal.Volume.from_name("vllm-model-cache", create_if_missing=True)
MODEL_CACHE_PATH = "/root/.cache/huggingface"

QWEN_7B_MODEL = "Qwen/Qwen2.5-7B-Instruct"
QWEN_72B_MODEL = "Qwen/Qwen2.5-72B-Instruct-AWQ"

# --- Images ---

web_image = (
    modal.Image.debian_slim(python_version="3.12")
    .apt_install("tesseract-ocr")
    .pip_install_from_requirements("requirements.txt")
    .add_local_dir("app", remote_path="/root/app")
)

# Pre-download model weights into the image so cold starts don't need to fetch them
vllm_image_7b = (
    modal.Image.debian_slim(python_version="3.12")
    .pip_install("vllm>=0.6.0", "torch>=2.4.0", "huggingface_hub")
    .run_commands(f"huggingface-cli download {QWEN_7B_MODEL}")
)

vllm_image_72b = (
    modal.Image.debian_slim(python_version="3.12")
    .pip_install("vllm>=0.6.0", "torch>=2.4.0", "huggingface_hub")
    .run_commands(f"huggingface-cli download {QWEN_72B_MODEL}")
)

# --- GPU classes ---


@app.cls(
    image=vllm_image_7b,
    gpu="A10G",
    volumes={MODEL_CACHE_PATH: model_cache},
    min_containers=0,
    scaledown_window=600,
    timeout=600,
    secrets=[modal.Secret.from_name("serve-funding-secrets")],
)
class Qwen7B:
    model_name: str = QWEN_7B_MODEL

    @modal.enter()
    def load_model(self):
        from vllm import LLM

        self.llm = LLM(
            model=self.model_name,
            trust_remote_code=True,
            max_model_len=4096,
        )

    @modal.method()
    def generate(self, system_prompt: str, user_message: str) -> str:
        from vllm import SamplingParams

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ]
        outputs = self.llm.chat(
            messages=[messages],
            sampling_params=SamplingParams(temperature=0.1, max_tokens=1024),
        )
        return outputs[0].outputs[0].text


@app.cls(
    image=vllm_image_72b,
    gpu="A100-80GB",
    volumes={MODEL_CACHE_PATH: model_cache},
    min_containers=0,
    scaledown_window=600,
    timeout=600,
    secrets=[modal.Secret.from_name("serve-funding-secrets")],
)
class Qwen72B:
    model_name: str = QWEN_72B_MODEL

    @modal.enter()
    def load_model(self):
        from vllm import LLM

        self.llm = LLM(
            model=self.model_name,
            trust_remote_code=True,
            quantization="awq",
            max_model_len=4096,
        )

    @modal.method()
    def generate(self, system_prompt: str, user_message: str) -> str:
        from vllm import SamplingParams

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ]
        outputs = self.llm.chat(
            messages=[messages],
            sampling_params=SamplingParams(temperature=0.1, max_tokens=1024),
        )
        return outputs[0].outputs[0].text


# --- Web endpoint (CPU only) ---


@app.function(
    image=web_image,
    secrets=[modal.Secret.from_name("serve-funding-secrets")],
    min_containers=0,
    timeout=600,
)
@modal.asgi_app()
def web():
    from app.main import app as fastapi_app

    return fastapi_app
