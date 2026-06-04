from app.providers.base import ProviderAdapter
from app.providers.openai import OpenAIAdapter
from app.providers.claude import ClaudeAdapter
from app.providers.gemini import GeminiAdapter


class ProviderFactory:
    """Factory for creating provider adapters."""

    @staticmethod
    def create(provider_name: str, api_key: str) -> ProviderAdapter:
        """Create a provider adapter instance.

        Args:
            provider_name: 'openai', 'claude', or 'gemini'
            api_key: The API key for the provider

        Returns:
            ProviderAdapter instance

        Raises:
            ValueError: If provider_name is not recognized
        """
        if provider_name == "openai":
            return OpenAIAdapter(api_key)
        elif provider_name == "claude":
            return ClaudeAdapter(api_key)
        elif provider_name == "gemini":
            return GeminiAdapter(api_key)
        else:
            raise ValueError(f"Unknown provider: {provider_name}")
