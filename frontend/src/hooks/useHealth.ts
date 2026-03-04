"use client";

import { useEffect, useState } from "react";
import type { HealthResponse } from "@/lib/types";
import { fetchHealth } from "@/lib/api";

export function useHealth(intervalMs = 30_000) {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [checked, setChecked] = useState(false);

  useEffect(() => {
    let mounted = true;

    const poll = async () => {
      try {
        const data = await fetchHealth();
        if (mounted) setHealth(data);
      } catch {
        if (mounted) setHealth(null);
      } finally {
        if (mounted) setChecked(true);
      }
    };

    poll();
    const id = setInterval(poll, intervalMs);
    return () => {
      mounted = false;
      clearInterval(id);
    };
  }, [intervalMs]);

  return { health, checked };
}
