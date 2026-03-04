"use client";

import { useCallback, useRef, useState } from "react";
import { useTemplates } from "@/hooks/useTemplates";
import { extractDocument } from "@/lib/api";
import type { ExtractionResponse } from "@/lib/types";
import ResultsTable from "./ResultsTable";
import CopyButton from "./CopyButton";
import StatsBar from "./StatsBar";

const ACCEPTED = ".pdf,.png,.jpg,.jpeg,.tiff,.tif,.bmp";

export default function ExtractionForm() {
  const { templates, loading: templatesLoading } = useTemplates();
  const [template, setTemplate] = useState("");
  const [threshold, setThreshold] = useState(0.7);
  const [file, setFile] = useState<File | null>(null);
  const [dragging, setDragging] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<ExtractionResponse | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Default to first template once loaded
  if (!template && templates.length > 0) {
    setTemplate(templates[0].name);
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file || !template) return;

    setLoading(true);
    setError(null);
    try {
      const data = await extractDocument(file, template, threshold);
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Extraction failed");
    } finally {
      setLoading(false);
    }
  };

  const onDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragging(false);
    const dropped = e.dataTransfer.files[0];
    if (dropped) setFile(dropped);
  }, []);

  return (
    <div className="space-y-6">
      <form onSubmit={handleSubmit} className="space-y-5">
        {/* Template */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Template
          </label>
          <select
            value={template}
            onChange={(e) => setTemplate(e.target.value)}
            disabled={templatesLoading}
            className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
          >
            {templates.map((t) => (
              <option key={t.name} value={t.name}>
                {t.description || t.name}
              </option>
            ))}
          </select>
        </div>

        {/* File upload */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Document
          </label>
          <div
            onDragOver={(e) => {
              e.preventDefault();
              setDragging(true);
            }}
            onDragLeave={() => setDragging(false)}
            onDrop={onDrop}
            onClick={() => inputRef.current?.click()}
            className={`flex cursor-pointer flex-col items-center justify-center rounded-lg border-2 border-dashed px-6 py-10 transition-colors ${
              dragging
                ? "border-blue-400 bg-blue-50"
                : "border-gray-300 hover:border-gray-400"
            }`}
          >
            <p className="text-sm text-gray-600">
              {file ? file.name : "Drop a file here, or click to browse"}
            </p>
            <p className="mt-1 text-xs text-gray-400">
              PDF, PNG, JPEG, TIFF, BMP
            </p>
            <input
              ref={inputRef}
              type="file"
              accept={ACCEPTED}
              className="hidden"
              onChange={(e) => setFile(e.target.files?.[0] ?? null)}
            />
          </div>
        </div>

        {/* Threshold */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Confidence Threshold: {threshold.toFixed(2)}
          </label>
          <input
            type="range"
            min={0}
            max={1}
            step={0.05}
            value={threshold}
            onChange={(e) => setThreshold(parseFloat(e.target.value))}
            className="w-full"
          />
        </div>

        {/* Submit */}
        <button
          type="submit"
          disabled={loading || !file}
          className="w-full rounded-lg bg-blue-600 px-4 py-2.5 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50 transition-colors"
        >
          {loading ? (
            <span className="inline-flex items-center gap-2">
              <span className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
              Extracting…
            </span>
          ) : (
            "Extract Data"
          )}
        </button>
      </form>

      {error && (
        <div className="rounded-lg bg-red-50 px-4 py-3 text-sm text-red-700">
          {error}
        </div>
      )}

      {result && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold text-gray-900">Results</h2>
            <CopyButton results={result.results} />
          </div>
          <StatsBar stats={result.stats} />
          <ResultsTable results={result.results} threshold={result.threshold} />
        </div>
      )}
    </div>
  );
}
