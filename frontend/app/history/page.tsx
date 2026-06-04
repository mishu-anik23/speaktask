"use client";

import { useState } from "react";
import { ProtectedLayout } from "@/components/ProtectedLayout";
import { HistoryList } from "@/components/HistoryList";
import { Command } from "@/lib/types";
import Link from "next/link";

export default function HistoryPage() {
  const [selectedCommand, setSelectedCommand] = useState<Command | null>(null);

  return (
    <ProtectedLayout>
      <div className="min-h-screen bg-gray-50">
        <header className="bg-white border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
            <h1 className="text-2xl font-bold">SpeakTask</h1>
            <nav className="space-x-4">
              <Link href="/dashboard" className="text-gray-600 hover:text-gray-900">
                Dashboard
              </Link>
              <Link href="/history" className="text-blue-600 font-medium">
                History
              </Link>
              <Link href="/settings" className="text-gray-600 hover:text-gray-900">
                Settings
              </Link>
              <button
                onClick={() => {
                  localStorage.removeItem("token");
                  window.location.href = "/login";
                }}
                className="text-gray-600 hover:text-gray-900"
              >
                Logout
              </button>
            </nav>
          </div>
        </header>

        <main className="max-w-7xl mx-auto px-4 py-8">
          <div className="bg-white rounded-lg shadow p-8">
            <h2 className="text-xl font-semibold mb-6">Command History</h2>
            <HistoryList onCommandClick={setSelectedCommand} />
          </div>

          {selectedCommand && (
            <div className="mt-8 bg-white rounded-lg shadow p-8">
              <div className="flex justify-between items-start mb-6">
                <div>
                  <h3 className="text-lg font-semibold mb-2">Command Details</h3>
                  <p className="text-gray-600">{selectedCommand.raw_input}</p>
                </div>
                <button
                  onClick={() => setSelectedCommand(null)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  ✕
                </button>
              </div>

              {selectedCommand.runs && selectedCommand.runs.length > 0 && (
                <div className="space-y-4">
                  {selectedCommand.runs.map((run) => (
                    <div key={run.id} className="border-t pt-4">
                      <div className="text-sm text-gray-600 mb-2">
                        Started: {new Date(run.started_at).toLocaleString()}
                      </div>
                      {run.result_text && (
                        <div className="p-4 bg-gray-50 rounded border border-gray-200">
                          <p className="text-sm font-medium mb-2">Result:</p>
                          <p className="text-sm whitespace-pre-wrap">{run.result_text}</p>
                        </div>
                      )}
                      {run.error_message && (
                        <div className="p-4 bg-red-50 rounded border border-red-200">
                          <p className="text-sm font-medium text-red-800 mb-2">Error:</p>
                          <p className="text-sm text-red-700">{run.error_message}</p>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </main>
      </div>
    </ProtectedLayout>
  );
}
