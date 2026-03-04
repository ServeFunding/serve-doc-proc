"use client";

import AuthGate from "@/components/AuthGate";
import ExtractionForm from "@/components/ExtractionForm";
import HealthBadge from "@/components/HealthBadge";
import { useAuth } from "@/hooks/useAuth";

function AppContent() {
  const { signOut } = useAuth();

  return (
    <div className="min-h-screen">
      <header className="border-b border-gray-200 bg-white">
        <div className="mx-auto flex max-w-3xl items-center justify-between px-4 py-3">
          <h1 className="text-lg font-semibold text-gray-900">
            Serve Funding Deal Manager
          </h1>
          <div className="flex items-center gap-3">
            <HealthBadge />
            <button
              onClick={signOut}
              className="text-sm text-gray-500 hover:text-gray-700"
            >
              Logout
            </button>
          </div>
        </div>
      </header>
      <main className="mx-auto max-w-3xl px-4 py-8">
        <ExtractionForm />
      </main>
    </div>
  );
}

export default function Home() {
  return (
    <AuthGate>
      <AppContent />
    </AuthGate>
  );
}
