from ..config import get_settings
from .base import BaseLLMProvider
from .deepseek_provider import DeepSeekProvider
from .kimi_provider import KimiProvider
from .mock_provider import MockProvider
from .openai_provider import OpenAIProvider
from .qwen_provider import QwenProvider
from .zhipu_provider import ZhipuProvider


def get_llm_provider() -> BaseLLMProvider:
    settings = get_settings()
    provider = (settings.llm_provider or "mock").lower().strip()
    model = settings.llm_model

    if provider in {"mock", "rule", "none", ""}:
        return MockProvider(model=model)
    if provider == "openai":
        return OpenAIProvider(api_key=settings.openai_api_key, model=model)
    if provider == "deepseek":
        return DeepSeekProvider(api_key=settings.deepseek_api_key, model=model)
    if provider == "qwen":
        return QwenProvider(api_key=settings.qwen_api_key, model=model)
    if provider == "kimi":
        return KimiProvider(api_key=settings.kimi_api_key, model=model)
    if provider in {"zhipu", "glm", "zhipu_glm"}:
        return ZhipuProvider(api_key=settings.zhipu_api_key, model=model)

    return MockProvider(model=model)
