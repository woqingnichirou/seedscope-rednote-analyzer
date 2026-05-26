from .openai_compatible import OpenAICompatibleProvider


class QwenProvider(OpenAICompatibleProvider):
    name = "qwen"
    default_model = "qwen-plus"
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
