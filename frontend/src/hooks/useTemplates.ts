"use client";

import { useEffect, useState } from "react";
import type { TemplateInfo } from "@/lib/types";
import { fetchTemplates } from "@/lib/api";

export function useTemplates() {
  const [templates, setTemplates] = useState<TemplateInfo[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTemplates()
      .then((data) => setTemplates(data.templates))
      .catch(() => setTemplates([]))
      .finally(() => setLoading(false));
  }, []);

  return { templates, loading };
}
