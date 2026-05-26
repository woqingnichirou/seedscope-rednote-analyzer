class LLMClient:
    """Backward-compatible wrapper around the provider factory."""

    def summarize(self, prompt: str) -> dict:
        from ..llm.factory import get_llm_provider

        provider = get_llm_provider()
        if not provider.is_configured:
            return {}
        try:
            return provider.complete_json(prompt)
        except Exception:
            return {}
