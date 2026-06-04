"use client";

import { useState } from "react";
import { useVoiceRecorder } from "@/hooks/useVoiceRecorder";
import { api } from "@/lib/api";

interface MicButtonProps {
  onCommandSubmitted?: (commandId: number) => void;
  selectedProvider?: string;
}

export function MicButton({ onCommandSubmitted, selectedProvider }: MicButtonProps) {
  const { isRecording, startRecording, stopRecording, error } = useVoiceRecorder();
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleClick = async () => {
    if (isRecording) {
      setIsSubmitting(true);
      try {
        const audioBlob = await stopRecording();
        const formData = new FormData();
        formData.append("file", audioBlob, "audio.wav");
        if (selectedProvider) {
          formData.append("selected_provider", selectedProvider);
        }

        const response = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL}/voice/submit`,
          {
            method: "POST",
            headers: {
              Authorization: `Bearer ${localStorage.getItem("token")}`,
            },
            body: formData,
          }
        );

        if (response.ok) {
          const data = await response.json();
          onCommandSubmitted?.(data.command_id);
        }
      } catch (err) {
        console.error("Failed to submit audio:", err);
      } finally {
        setIsSubmitting(false);
      }
    } else {
      await startRecording();
    }
  };

  return (
    <div className="flex flex-col items-center gap-4">
      <button
        onClick={handleClick}
        disabled={isSubmitting}
        className={`relative w-20 h-20 rounded-full transition-all ${
          isRecording
            ? "bg-red-500 hover:bg-red-600 animate-pulse"
            : "bg-blue-600 hover:bg-blue-700"
        } disabled:opacity-50 disabled:cursor-not-allowed text-white font-semibold`}
      >
        {isRecording ? "⏹" : "🎤"}
      </button>
      {isRecording && (
        <p className="text-sm text-red-600 font-medium">Recording...</p>
      )}
      {error && (
        <p className="text-sm text-red-600">{error}</p>
      )}
    </div>
  );
}
