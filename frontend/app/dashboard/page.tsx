"use client";

import { useState } from "react";
import { ProtectedLayout } from "@/components/ProtectedLayout";
import { MicButton } from "@/components/MicButton";
import { CommandInput } from "@/components/CommandInput";
import { OutputPanel } from "@/components/OutputPanel";
import Link from "next/link";

export default function DashboardPage() {
  const [currentCommandId, setCurrentCommandId] = useState<number | null>(null);
  const [selectedProvider, setSelectedProvider] = useState("openai");

  return (
    <ProtectedLayout>
      <div className="min-h-screen bg-gray-50">
        <header className="bg-white border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
            <h1 className="text-2xl font-bold">SpeakTask</h1>
            <nav className="space-x-4">
              <Link href="/dashboard" className="text-blue-600 font-medium">
                Dashboard
              </Link>
              <Link href="/history" className="text-gray-600 hover:text-gray-900">
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
          <div className="bg-white rounded-lg shadow p-8 mb-8">
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Provider
              </label>
              <select
                value={selectedProvider}
                onChange={(e) => setSelectedProvider(e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              >
                <option value="openai">OpenAI</option>
                <option value="claude">Claude</option>
                <option value="gemini">Gemini</option>
              </select>
            </div>

            <div className="flex flex-col items-center gap-8 py-8">
              <MicButton
                selectedProvider={selectedProvider}
                onCommandSubmitted={setCurrentCommandId}
              />
              <div className="text-gray-400">or</div>
              <CommandInput
                selectedProvider={selectedProvider}
                onCommandSubmitted={setCurrentCommandId}
              />
            </div>
          </div>

          {currentCommandId && (
            <OutputPanel commandId={currentCommandId} />
          )}
        </main>
      </div>
    </ProtectedLayout>
  );
}
