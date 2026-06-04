"use client";

import { useState, useEffect } from "react";

interface OutputPanelProps {
  commandId?: number;
}

export function OutputPanel({ commandId }: OutputPanelProps) {
  const [status, setStatus] = useState<string>("queued");
  const [result, setResult] = useState<string>("");
  const [error, setError] = useState<string>("");
  const [ws, setWs] = useState<WebSocket | null>(null);

  useEffect(() => {
    if (!commandId) return;

    const token = localStorage.getItem("token");
    const wsUrl = `${process.env.NEXT_PUBLIC_WS_URL}/ws/commands?command_id=${commandId}&token=${token}`;

    const websocket = new WebSocket(wsUrl);

    websocket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.status) {
          setStatus(data.status);
        }
        if (data.result) {
          setResult(data.result);
        }
        if (data.error) {
          setError(data.error);
        }
      } catch (e) {
        console.error("Failed to parse message:", e);
      }
    };

    websocket.onerror = () => {
      setError("Connection lost");
    };

    setWs(websocket);

    return () => {
      websocket.close();
    };
  }, [commandId]);

  if (!commandId) {
    return (
      <div className="w-full max-w-2xl mx-auto p-6 bg-gray-50 rounded-lg border border-gray-200">
        <p className="text-gray-500">Submit a command to see results here</p>
      </div>
    );
  }

  return (
    <div className="w-full max-w-2xl mx-auto p-6 bg-white rounded-lg border border-gray-200">
      <div className="mb-4">
        <h3 className="text-sm font-semibold text-gray-700 mb-2">Status</h3>
        <p className="px-3 py-1 bg-blue-50 text-blue-700 rounded-full inline-block text-sm font-medium">
          {status}
        </p>
      </div>

      {result && (
        <div className="mb-4">
          <h3 className="text-sm font-semibold text-gray-700 mb-2">Result</h3>
          <div className="p-4 bg-gray-50 rounded border border-gray-200 text-sm whitespace-pre-wrap">
            {result}
          </div>
        </div>
      )}

      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded text-red-700 text-sm">
          {error}
        </div>
      )}
    </div>
  );
}
