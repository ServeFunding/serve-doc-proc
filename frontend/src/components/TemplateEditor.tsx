"use client";

import { useEffect, useState } from "react";
import { updateTemplate, resetTemplate } from "@/lib/api";

interface Row {
  key: string;
  question: string;
}

export default function TemplateEditor({
  templateName,
  questions,
  onSaved,
}: {
  templateName: string;
  questions: Record<string, string>;
  onSaved: () => void;
}) {
  const [rows, setRows] = useState<Row[]>([]);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  useEffect(() => {
    setRows(
      Object.entries(questions).map(([key, question]) => ({ key, question })),
    );
    setMessage(null);
  }, [questions, templateName]);

  const updateRow = (index: number, field: "key" | "question", value: string) => {
    setRows((prev) => {
      const next = [...prev];
      next[index] = { ...next[index], [field]: value };
      return next;
    });
  };

  const addRow = () => {
    setRows((prev) => [...prev, { key: "", question: "" }]);
  };

  const removeRow = (index: number) => {
    setRows((prev) => prev.filter((_, i) => i !== index));
  };

  const handleSave = async () => {
    const qs: Record<string, string> = {};
    for (const row of rows) {
      const k = row.key.trim();
      const q = row.question.trim();
      if (k && q) qs[k] = q;
    }
    if (Object.keys(qs).length === 0) return;

    setSaving(true);
    setMessage(null);
    try {
      await updateTemplate(templateName, qs);
      setMessage("Saved!");
      onSaved();
    } catch (err) {
      setMessage(err instanceof Error ? err.message : "Save failed");
    } finally {
      setSaving(false);
    }
  };

  const handleReset = async () => {
    setSaving(true);
    setMessage(null);
    try {
      await resetTemplate(templateName);
      setMessage("Reset to defaults");
      onSaved();
    } catch (err) {
      setMessage(err instanceof Error ? err.message : "Reset failed");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-3 rounded-lg border border-gray-200 bg-gray-50 p-4">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold text-gray-800">
          Edit Template Questions
        </h3>
        <span className="text-xs text-gray-500">{rows.length} fields</span>
      </div>

      <div className="max-h-80 space-y-2 overflow-y-auto">
        {rows.map((row, i) => (
          <div key={i} className="flex gap-2">
            <input
              value={row.key}
              onChange={(e) => updateRow(i, "key", e.target.value)}
              placeholder="field_key"
              className="w-40 shrink-0 rounded border border-gray-300 px-2 py-1.5 text-xs font-mono focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
            />
            <input
              value={row.question}
              onChange={(e) => updateRow(i, "question", e.target.value)}
              placeholder="Question text"
              className="flex-1 rounded border border-gray-300 px-2 py-1.5 text-xs focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
            />
            <button
              type="button"
              onClick={() => removeRow(i)}
              className="shrink-0 rounded px-2 py-1.5 text-xs text-red-600 hover:bg-red-50"
            >
              Remove
            </button>
          </div>
        ))}
      </div>

      <div className="flex items-center gap-2">
        <button
          type="button"
          onClick={addRow}
          className="rounded bg-gray-200 px-3 py-1.5 text-xs font-medium text-gray-700 hover:bg-gray-300"
        >
          + Add Field
        </button>
        <button
          type="button"
          onClick={handleSave}
          disabled={saving}
          className="rounded bg-blue-600 px-3 py-1.5 text-xs font-medium text-white hover:bg-blue-700 disabled:opacity-50"
        >
          {saving ? "Saving…" : "Save"}
        </button>
        <button
          type="button"
          onClick={handleReset}
          disabled={saving}
          className="rounded bg-gray-200 px-3 py-1.5 text-xs font-medium text-gray-700 hover:bg-gray-300 disabled:opacity-50"
        >
          Reset to Default
        </button>
        {message && (
          <span className="text-xs text-gray-600">{message}</span>
        )}
      </div>
    </div>
  );
}
