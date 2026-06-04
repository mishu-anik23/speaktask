"use client";

import { useState } from "react";

interface ProviderConnectionCardProps {
  provider: "openai" | "claude" | "gemini";
  isConnected: boolean;
  onConnect?: (apiKey: string) => void;
  onDisconnect?: () => void;
}

export function ProviderConnectionCard({
  provider,
  isConnected,
  onConnect,
  onDisconnect,
}: ProviderConnectionCardProps) {
  const [isExpanded, setIsExpanded] = useState(false);
  const [apiKey, setApiKey] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const providerInfo = {
    openai: {
      label: "OpenAI",
      color: "green",
      docsUrl: "https://platform.openai.com/api-keys",
    },
    claude: {
      label: "Anthropic Claude",
      color: "amber",
      docsUrl: "https://console.anthropic.com/",
    },
    gemini: {
      label: "Google Gemini",
      color: "blue",
      docsUrl: "https://aistudio.google.com/app/apikey",
    },
  };

  const info = providerInfo[provider];

  const handleConnect = async () => {
    if (!apiKey.trim()) return;
    setIsLoading(true);
    try {
      await onConnect?.(apiKey);
      setApiKey("");
      setIsExpanded(false);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDisconnect = async () => {
    setIsLoading(true);
    try {
      await onDisconnect?.();
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="border border-gray-200 rounded-lg p-4">
      <div className="flex justify-between items-center">
        <div className="flex items-center gap-3">
          <div className={`w-3 h-3 rounded-full bg-${info.color}-500`}></div>
          <span className="font-medium">{info.label}</span>
        </div>
        <div>
          {isConnected ? (
            <>
              <span className="text-sm text-green-600 font-medium">Connected</span>
              <button
                onClick={handleDisconnect}
                disabled={isLoading}
                className="ml-4 px-3 py-1 text-sm border border-red-300 text-red-600 rounded hover:bg-red-50 disabled:opacity-50"
              >
                Disconnect
              </button>
            </>
          ) : (
            <button
              onClick={() => setIsExpanded(!isExpanded)}
              className="px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              Connect
            </button>
          )}
        </div>
      </div>

      {isExpanded && !isConnected && (
        <div className="mt-4 space-y-3">
          <input
            type="password"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            placeholder="Enter API key"
            className="w-full px-3 py-2 border border-gray-300 rounded text-sm"
          />
          <div className="flex gap-2">
            <button
              onClick={handleConnect}
              disabled={isLoading || !apiKey.trim()}
              className="px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
            >
              {isLoading ? "Saving..." : "Save"}
            </button>
            <button
              onClick={() => setIsExpanded(false)}
              className="px-3 py-1 text-sm border border-gray-300 text-gray-600 rounded hover:bg-gray-50"
            >
              Cancel
            </button>
          </div>
          <a
            href={info.docsUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="text-xs text-blue-600 hover:underline block"
          >
            Get API key →
          </a>
        </div>
      )}
    </div>
  );
}
