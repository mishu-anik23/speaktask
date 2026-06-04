"use client";

import { useState, useEffect } from "react";
import { Command } from "@/lib/types";

interface HistoryListProps {
  onCommandClick?: (command: Command) => void;
}

export function HistoryList({ onCommandClick }: HistoryListProps) {
  const [commands, setCommands] = useState<Command[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [filter, setFilter] = useState("");

  useEffect(() => {
    const fetchCommands = async () => {
      try {
        const params = filter ? `?provider=${filter}` : "";
        const response = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL}/commands${params}`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("token")}`,
            },
          }
        );
        if (response.ok) {
          const data = await response.json();
          setCommands(data);
        }
      } catch (err) {
        console.error("Failed to fetch commands:", err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchCommands();
  }, [filter]);

  const getStatusColor = (status: string) => {
    switch (status) {
      case "succeeded":
        return "bg-green-100 text-green-800";
      case "failed":
        return "bg-red-100 text-red-800";
      case "processing":
        return "bg-blue-100 text-blue-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  if (isLoading) {
    return <div className="text-center py-8 text-gray-500">Loading...</div>;
  }

  if (commands.length === 0) {
    return <div className="text-center py-8 text-gray-500">No commands yet</div>;
  }

  return (
    <div>
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Filter by Provider
        </label>
        <select
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="px-3 py-2 border border-gray-300 rounded-lg"
        >
          <option value="">All Providers</option>
          <option value="openai">OpenAI</option>
          <option value="claude">Claude</option>
          <option value="gemini">Gemini</option>
        </select>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead className="border-b border-gray-200">
            <tr>
              <th className="text-left py-3 px-4">Input</th>
              <th className="text-left py-3 px-4">Provider</th>
              <th className="text-left py-3 px-4">Status</th>
              <th className="text-left py-3 px-4">Date</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {commands.map((cmd) => (
              <tr
                key={cmd.id}
                onClick={() => onCommandClick?.(cmd)}
                className="hover:bg-gray-50 cursor-pointer"
              >
                <td className="py-3 px-4 truncate max-w-xs">
                  {cmd.raw_input.substring(0, 50)}...
                </td>
                <td className="py-3 px-4">{cmd.selected_provider}</td>
                <td className="py-3 px-4">
                  <span className={`px-2 py-1 rounded text-xs font-medium ${getStatusColor(cmd.status)}`}>
                    {cmd.status}
                  </span>
                </td>
                <td className="py-3 px-4 text-gray-500">
                  {new Date(cmd.created_at).toLocaleDateString()}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
