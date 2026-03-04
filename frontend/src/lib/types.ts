export interface QuestionResult {
  answer: string;
  confidence: number;
}

export interface ExtractionStats {
  total_questions: number;
  above_threshold: number;
  below_threshold: number;
  processing_time_seconds: number;
}

export interface ExtractionResponse {
  template: string;
  threshold: number;
  model: string;
  results: Record<string, QuestionResult>;
  filtered_results: Record<string, string>;
  stats: ExtractionStats;
}

export interface TemplateInfo {
  name: string;
  description: string;
  questions: Record<string, string>;
}

export interface TemplateListResponse {
  templates: TemplateInfo[];
}

export interface HealthResponse {
  status: string;
  provider: string;
  provider_connected: boolean;
  model: string;
}
