from typing import Any

from .base import BaseLLMProvider


class MockProvider(BaseLLMProvider):
    name = "mock"
    default_model = "mock-local-demo"

    def complete_json(self, prompt: str, schema_hint: str | None = None) -> dict[str, Any]:
        if "content_type" in (schema_hint or ""):
            return {
                "content_type": "选课决策型",
                "title_type": "问题先行",
                "cover_type": "选课避坑型",
                "body_structure": "立人设 → 讲痛点 → 抛认知 → 引品牌 → 给结果 → 接 CTA",
                "cta_type": "评论承接",
            }
        return {
            "summary": "mock provider 已启用。当前结果用于本地 demo，不调用真实模型。",
            "insights": [
                "优先提升决策型内容比例。",
                "减少品牌前置标题，增加问题和方法入口。",
                "将高赞素材沉淀为复投白名单。",
            ],
        }
