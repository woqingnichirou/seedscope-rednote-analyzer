from .openai_compatible import OpenAICompatibleProvider


class DeepSeekProvider(OpenAICompatibleProvider):
    name = "deepseek"
    default_model = "deepseek-chat"
    base_url = "https://api.deepseek.com"
