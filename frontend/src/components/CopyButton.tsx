"use client";

import { useState } from "react";
import type { EntityResult, QuestionResult } from "@/lib/types";

export default function CopyButton({
  results,
  entities,
}: {
  results: Record<string, QuestionResult>;
  entities?: EntityResult[];
}) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    let tsv: string;

    if (entities && entities.length > 0) {
      const header = "Entity\tField\tAnswer\tConfidence";
      const rows = entities.flatMap((entity) =>
        Object.entries(entity.results).map(
          ([field, { answer, confidence }]) =>
            `${entity.name}\t${field}\t${answer}\t${confidence.toFixed(2)}`,
        ),
      );
      tsv = [header, ...rows].join("\n");
    } else {
      const header = "Field\tAnswer\tConfidence";
      const rows = Object.entries(results).map(
        ([field, { answer, confidence }]) =>
          `${field}\t${answer}\t${confidence.toFixed(2)}`,
      );
      tsv = [header, ...rows].join("\n");
    }

    await navigator.clipboard.writeText(tsv);
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
