import type { ExtractionStats } from "@/lib/types";

export default function StatsBar({ stats }: { stats: ExtractionStats }) {
  return (
    <div className="flex flex-wrap gap-4 rounded-lg bg-gray-50 px-4 py-3 text-sm text-gray-700">
      <span>
        <strong>{stats.total_questions}</strong> fields
      </span>
      <span className="text-green-700">
        <strong>{stats.above_threshold}</strong> above threshold
      </span>
      <span className="text-red-700">
        <strong>{stats.below_threshold}</strong> below threshold
      </span>
      <span className="text-gray-500">
        {stats.processing_time_seconds.toFixed(1)}s
      </span>
    </div>
  );
}
