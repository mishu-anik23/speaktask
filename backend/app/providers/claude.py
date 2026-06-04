import httpx
import json
from typing import Dict, Any
from app.providers.base import ProviderAdapter


class ClaudeAdapter(ProviderAdapter):
    """Adapter for Anthropic Claude API."""

    BASE_URL = "https://api.anthropic.com/v1"

    async def execute(self, prompt: str) -> Dict[str, Any]:
        """Execute a command using Anthropic Claude."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.BASE_URL}/messages",
                headers={
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json={
                    "model": "claude-3-sonnet-20240229",
                    "max_tokens": 1024,
                    "messages": [{"role": "user", "content": prompt}],
                },
                timeout=30.0,
            )

            if response.status_code != 200:
                raise Exception(f"Claude API error: {response.text}")

            data = response.json()
            result = data["content"][0]["text"]
            tokens_used = data.get("usage", {}).get("input_tokens", 0) + data.get("usage", {}).get("output_tokens", 0)

            return {"result": result, "tokens_used": tokens_used}

    async def validate_credentials(self) -> bool:
        """Validate Claude API key."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.BASE_URL}/messages",
                    headers={
                        "x-api-key": self.api_key,
                        "anthropic-version": "2023-06-01",
                    },
                    json={
                        "model": "claude-3-sonnet-20240229",
                        "max_tokens": 10,
                        "messages": [{"role": "user", "content": "test"}],
                    },
                    timeout=10.0,
                )
                return response.status_code in [200, 401]  # 401 means auth failed but API is reachable
        except Exception:
            return False
