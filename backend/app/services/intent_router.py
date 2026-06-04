class IntentRouter:
    """Simple keyword-based intent router for commands."""

    PROVIDER_KEYWORDS = {
        "openai": ["openai", "gpt", "chatgpt"],
        "claude": ["claude", "anthropic"],
        "gemini": ["gemini", "google"],
    }

    @staticmethod
    def route(transcript: str, default_provider: str = "openai") -> str:
        """Route a command to the best provider based on keywords.

        Args:
            transcript: The command transcript/text
            default_provider: The default provider if no keywords match

        Returns:
            Provider name: 'openai', 'claude', or 'gemini'
        """
        transcript_lower = transcript.lower()

        for provider, keywords in IntentRouter.PROVIDER_KEYWORDS.items():
            for keyword in keywords:
                if keyword in transcript_lower:
                    return provider

        return default_provider

    @staticmethod
    def extract_intent(transcript: str) -> str:
        """Extract the command intent from the transcript.

        For v1, this is simplified to just return the transcript.
        In a future version, this could use an LLM to classify intents.
        """
        return transcript
