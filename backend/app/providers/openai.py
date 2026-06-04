import httpx
from typing import Dict, Any
from app.providers.base import ProviderAdapter


class OpenAIAdapter(ProviderAdapter):
    """Adapter for OpenAI API."""

    BASE_URL = "https://api.openai.com/v1"

    async def execute(self, prompt: str) -> Dict[str, Any]:
        """Execute a command using OpenAI ChatCompletion."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.BASE_URL}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": "gpt-3.5-turbo",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7,
                },
                timeout=30.0,
            )

            if response.status_code != 200:
                raise Exception(f"OpenAI API error: {response.text}")

            data = response.json()
            result = data["choices"][0]["message"]["content"]
            tokens_used = data.get("usage", {}).get("total_tokens", 0)

            return {"result": result, "tokens_used": tokens_used}

    async def validate_credentials(self) -> bool:
        """Validate OpenAI API key."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.BASE_URL}/models",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    timeout=10.0,
                )
                return response.status_code == 200
        except Exception:
            return False
