import json

from openai import OpenAI

from ..config import get_settings


class LLMClient:
    def summarize(self, prompt: str) -> dict:
        settings = get_settings()
        if settings.llm_provider.lower() == "openai" and settings.openai_api_key:
            client = OpenAI(api_key=settings.openai_api_key)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "你是资深 AI 产品经理，请输出严格 JSON。"},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.2,
            )
            content = response.choices[0].message.content or "{}"
            return json.loads(content)
        return {}


class DeepSeekClient(LLMClient):
    """Extension point for DeepSeek-compatible chat completions."""


class ClaudeClient(LLMClient):
    """Extension point for Claude Messages API."""
