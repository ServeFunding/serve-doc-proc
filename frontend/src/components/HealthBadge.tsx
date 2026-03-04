"use client";

import { useHealth } from "@/hooks/useHealth";

export default function HealthBadge() {
  const health = useHealth();

  const connected = health?.provider_connected ?? false;
  const label = connected ? health!.model : "Disconnected";

  return (
    <span className="inline-flex items-center gap-1.5 rounded-full border border-gray-200 px-2.5 py-0.5 text-xs text-gray-600">
      <span
        className={`h-2 w-2 rounded-full ${connected ? "bg-green-500" : "bg-red-500"}`}
      />
      {label}
    </span>
  );
}
