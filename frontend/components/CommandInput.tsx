"use client";

import { useState } from "react";
import { api } from "@/lib/api";

interface CommandInputProps {
  onCommandSubmitted?: (commandId: number) => void;
  selectedProvider?: string;
}

export function CommandInput({ onCommandSubmitted, selectedProvider }: CommandInputProps) {
  const [input, setInput] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    setIsSubmitting(true);
    setError("");

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/commands`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
          body: JSON.stringify({
            input_type: "text",
            raw_input: input,
            selected_provider: selectedProvider || "openai",
          }),
        }
      );

      if (response.ok) {
        const data = await response.json();
        setInput("");
        onCommandSubmitted?.(data.id);
      } else {
        setError("Failed to submit command");
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-2xl mx-auto">
      <div className="flex gap-2">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={isSubmitting}
          className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
          rows={3}
          placeholder="Type a command or question..."
        />
        <button
          type="submit"
          disabled={isSubmitting || !input.trim()}
          className="px-6 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition"
        >
          {isSubmitting ? "Sending..." : "Send"}
        </button>
      </div>
      {error && (
        <p className="text-sm text-red-600 mt-2">{error}</p>
      )}
    </form>
  );
}
