"use client";

import { useHealth } from "@/hooks/useHealth";

export default function HealthBadge() {
  const { health, checked } = useHealth();

  const reachable = health !== null;
  const connected = health?.provider_connected ?? false;

  let label: string;
  let dotColor: string;

  if (!checked) {
    label = "Checking…";
    dotColor = "bg-yellow-400";
  } else if (!reachable) {
    label = "Disconnected";
    dotColor = "bg-red-500";
  } else if (connected) {
    label = health!.model || "Connected";
    dotColor = "bg-green-500";
  } else {
    // Backend reachable but LLM provider not connected
    label = "Connected";
    dotColor = "bg-yellow-500";
  }

  return (
    <span className="inline-flex items-center gap-1.5 rounded-full border border-gray-200 px-2.5 py-0.5 text-xs text-gray-600">
      <span className={`h-2 w-2 rounded-full ${dotColor}`} />
      {label}
    </span>
  );
}
