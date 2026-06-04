"use client";

import { useState, useEffect } from "react";
import { ProtectedLayout } from "@/components/ProtectedLayout";
import { ProviderConnectionCard } from "@/components/ProviderConnectionCard";
import Link from "next/link";

export default function SettingsPage() {
  const [defaultProvider, setDefaultProvider] = useState("openai");
  const [connectedProviders, setConnectedProviders] = useState<Record<string, boolean>>({});
  const [isLoading, setIsLoading] = useState(false);

  const handleConnect = async (provider: string, apiKey: string) => {
    setIsLoading(true);
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/providers/connect`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
          body: JSON.stringify({
            provider_name: provider,
            credentials: { api_key: apiKey },
          }),
        }
      );

      if (response.ok) {
        setConnectedProviders((prev) => ({ ...prev, [provider]: true }));
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleDisconnect = async (provider: string) => {
    setIsLoading(true);
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/providers/disconnect?provider_name=${provider}`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      );

      if (response.ok) {
        setConnectedProviders((prev) => ({ ...prev, [provider]: false }));
      }
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const response = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL}/providers/status`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("token")}`,
            },
          }
        );
        if (response.ok) {
          const data = await response.json();
          setConnectedProviders(data);
        }
      } catch (err) {
        console.error("Failed to fetch provider status:", err);
      }
    };

    fetchStatus();
  }, []);

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
              <Link href="/history" className="text-gray-600 hover:text-gray-900">
                History
              </Link>
              <Link href="/settings" className="text-blue-600 font-medium">
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

        <main className="max-w-2xl mx-auto px-4 py-8">
          <div className="bg-white rounded-lg shadow p-8 mb-8">
            <h2 className="text-xl font-semibold mb-6">AI Provider Setup</h2>

            <div className="space-y-4 mb-8">
              <ProviderConnectionCard
                provider="openai"
                isConnected={connectedProviders.openai || false}
                onConnect={(key) => handleConnect("openai", key)}
                onDisconnect={() => handleDisconnect("openai")}
              />
              <ProviderConnectionCard
                provider="claude"
                isConnected={connectedProviders.claude || false}
                onConnect={(key) => handleConnect("claude", key)}
                onDisconnect={() => handleDisconnect("claude")}
              />
              <ProviderConnectionCard
                provider="gemini"
                isConnected={connectedProviders.gemini || false}
                onConnect={(key) => handleConnect("gemini", key)}
                onDisconnect={() => handleDisconnect("gemini")}
              />
            </div>

            <hr className="my-8" />

            <div>
              <h3 className="text-lg font-semibold mb-4">Preferences</h3>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Default Provider
                </label>
                <select
                  value={defaultProvider}
                  onChange={(e) => setDefaultProvider(e.target.value)}
                  className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                >
                  <option value="openai">OpenAI</option>
                  <option value="claude">Claude</option>
                  <option value="gemini">Gemini</option>
                </select>
              </div>
            </div>
          </div>
        </main>
      </div>
    </ProtectedLayout>
  );
}
