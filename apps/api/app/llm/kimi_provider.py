from .openai_compatible import OpenAICompatibleProvider


class KimiProvider(OpenAICompatibleProvider):
    name = "kimi"
    default_model = "moonshot-v1-8k"
    base_url = "https://api.moonshot.cn/v1"
