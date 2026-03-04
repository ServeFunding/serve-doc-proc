"use client";

import { useState } from "react";
import type { QuestionResult } from "@/lib/types";

export default function CopyButton({
  results,
}: {
  results: Record<string, QuestionResult>;
}) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    const header = "Field\tAnswer\tConfidence";
    const rows = Object.entries(results).map(
      ([field, { answer, confidence }]) =>
        `${field}\t${answer}\t${confidence.toFixed(2)}`,
    );
    await navigator.clipboard.writeText([header, ...rows].join("\n"));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <button
      onClick={handleCopy}
      className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 transition-colors"
    >
      {copied ? "Copied!" : "Copy to Spreadsheet"}
    </button>
  );
}
