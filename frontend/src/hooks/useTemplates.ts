"use client";

import { useCallback, useEffect, useState } from "react";
import type { TemplateInfo } from "@/lib/types";
import { fetchTemplates } from "@/lib/api";

export function useTemplates() {
  const [templates, setTemplates] = useState<TemplateInfo[]>([]);
  const [loading, setLoading] = useState(true);

  const refetch = useCallback(() => {
    setLoading(true);
    fetchTemplates()
      .then((data) => setTemplates(data.templates))
      .catch(() => setTemplates([]))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    refetch();
  }, [refetch]);

  return { templates, loading, refetch };
}
