import json
from typing import Any

from openai import OpenAI

from .base import BaseLLMProvider, LLMProviderError


class OpenAICompatibleProvider(BaseLLMProvider):
    base_url: str | None = None

    def complete_json(self, prompt: str, schema_hint: str | None = None) -> dict[str, Any]:
        if not self.api_key:
            raise LLMProviderError(f"{self.name} API key is not configured")

        messages = [
            {"role": "system", "content": "You are a precise marketing analysis assistant. Return strict JSON only."},
            {"role": "user", "content": prompt},
        ]
        if schema_hint:
            messages.insert(1, {"role": "system", "content": f"Expected JSON shape: {schema_hint}"})

        client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.2,
            response_format={"type": "json_object"},
        )
        content = response.choices[0].message.content or "{}"
        try:
            return json.loads(content)
        except json.JSONDecodeError as exc:
            raise LLMProviderError(f"{self.name} returned invalid JSON") from exc
