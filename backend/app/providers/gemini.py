import httpx
from typing import Dict, Any
from app.providers.base import ProviderAdapter


class GeminiAdapter(ProviderAdapter):
    """Adapter for Google Gemini API."""

    BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"

    async def execute(self, prompt: str) -> Dict[str, Any]:
        """Execute a command using Google Gemini."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.BASE_URL}/gemini-pro:generateContent",
                params={"key": self.api_key},
                json={
                    "contents": [
                        {
                            "parts": [{"text": prompt}]
                        }
                    ],
                    "generationConfig": {
                        "temperature": 0.7,
                        "maxOutputTokens": 1024,
                    },
                },
                timeout=30.0,
            )

            if response.status_code != 200:
                raise Exception(f"Gemini API error: {response.text}")

            data = response.json()
            result = data["candidates"][0]["content"]["parts"][0]["text"]
            tokens_used = data.get("usageMetadata", {}).get("totalTokenCount", 0)

            return {"result": result, "tokens_used": tokens_used}

    async def validate_credentials(self) -> bool:
        """Validate Google Gemini API key."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.BASE_URL}/gemini-pro:generateContent",
                    params={"key": self.api_key},
                    json={
                        "contents": [
                            {
                                "parts": [{"text": "test"}]
                            }
                        ]
                    },
                    timeout=10.0,
                )
                return response.status_code == 200
        except Exception:
            return False
