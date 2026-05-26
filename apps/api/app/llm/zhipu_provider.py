from .openai_compatible import OpenAICompatibleProvider


class ZhipuProvider(OpenAICompatibleProvider):
    name = "zhipu"
    default_model = "glm-4-flash"
    base_url = "https://open.bigmodel.cn/api/paas/v4"

    # TODO: Verify response_format behavior against the latest Zhipu GLM API.
    # The provider is intentionally OpenAI-compatible first so app startup does not depend
    # on provider-specific SDKs.
