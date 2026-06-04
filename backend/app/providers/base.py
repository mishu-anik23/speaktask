from abc import ABC, abstractmethod
from typing import Dict, Any


class ProviderAdapter(ABC):
    """Base class for all AI provider adapters."""

    def __init__(self, api_key: str):
        self.api_key = api_key

    @abstractmethod
    async def execute(self, prompt: str) -> Dict[str, Any]:
        """Execute a command with the provider.

        Returns:
            Dict with 'result' (str) and 'tokens_used' (int) keys.
        """
        pass

    @abstractmethod
    async def validate_credentials(self) -> bool:
        """Validate that the API key works."""
        pass
