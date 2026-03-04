import type { QuestionResult } from "@/lib/types";

function confidenceColor(confidence: number, threshold: number): string {
  if (confidence >= threshold) return "text-green-700 bg-green-50";
  if (confidence >= threshold * 0.75) return "text-yellow-700 bg-yellow-50";
  return "text-red-700 bg-red-50";
}

export default function ResultsTable({
  results,
  threshold,
}: {
  results: Record<string, QuestionResult>;
  threshold: number;
}) {
  const entries = Object.entries(results);

  return (
    <div className="overflow-x-auto rounded-lg border border-gray-200">
      <table className="w-full text-sm">
        <thead className="bg-gray-50 text-left text-gray-600">
          <tr>
            <th className="px-4 py-3 font-medium">Field</th>
            <th className="px-4 py-3 font-medium">Answer</th>
            <th className="px-4 py-3 font-medium w-28">Confidence</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-100">
          {entries.map(([field, { answer, confidence }]) => {
            const dimmed = confidence < threshold;
            return (
              <tr
                key={field}
                className={dimmed ? "opacity-50" : ""}
              >
                <td className="px-4 py-2.5 font-medium text-gray-900">
                  {field}
                </td>
                <td className="px-4 py-2.5 text-gray-700">{answer}</td>
                <td className="px-4 py-2.5">
                  <span
                    className={`inline-block rounded px-2 py-0.5 text-xs font-medium ${confidenceColor(confidence, threshold)}`}
                  >
                    {(confidence * 100).toFixed(0)}%
                  </span>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
