import type {
  ExtractionResponse,
  HealthResponse,
  TemplateListResponse,
} from "./types";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "";
const API_KEY = process.env.NEXT_PUBLIC_API_KEY ?? "";

function headers(): HeadersInit {
  return {
    Authorization: `Bearer ${API_KEY}`,
  };
}

export async function fetchHealth(): Promise<HealthResponse> {
  const res = await fetch(`${API_URL}/health`, { headers: headers() });
  if (!res.ok) throw new Error(`Health check failed: ${res.status}`);
  return res.json();
}

export async function fetchTemplates(): Promise<TemplateListResponse> {
  const res = await fetch(`${API_URL}/templates`, { headers: headers() });
  if (!res.ok) throw new Error(`Failed to fetch templates: ${res.status}`);
  return res.json();
}

export async function extractDocument(
  file: File,
  template: string,
  threshold: number,
  model: string = "",
  multiEntity: boolean = false,
): Promise<ExtractionResponse> {
  const form = new FormData();
  form.append("file", file);
  form.append("template", template);
  form.append("threshold", threshold.toString());
  if (model) form.append("model", model);
  if (multiEntity) form.append("multi_entity", "true");

  const res = await fetch(`${API_URL}/extract`, {
    method: "POST",
    headers: headers(),
    body: form,
    signal: AbortSignal.timeout(5 * 60 * 1000), // 5 min for cold starts
  });

  if (!res.ok) {
    const body = await res.json().catch(() => null);
    throw new Error(body?.detail ?? `Extraction failed: ${res.status}`);
  }
  return res.json();
}

export async function updateTemplate(
  name: string,
  questions: Record<string, string>,
): Promise<void> {
  const res = await fetch(`${API_URL}/templates/${name}`, {
    method: "PUT",
    headers: { ...headers(), "Content-Type": "application/json" },
    body: JSON.stringify({ questions }),
  });
  if (!res.ok) {
    const body = await res.json().catch(() => null);
    throw new Error(body?.detail ?? `Failed to update template: ${res.status}`);
  }
}

export async function resetTemplate(name: string): Promise<void> {
  const res = await fetch(`${API_URL}/templates/${name}/custom`, {
    method: "DELETE",
    headers: headers(),
  });
  if (!res.ok) {
    const body = await res.json().catch(() => null);
    throw new Error(body?.detail ?? `Failed to reset template: ${res.status}`);
  }
}
