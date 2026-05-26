from abc import ABC, abstractmethod
from typing import Any


class LLMProviderError(RuntimeError):
    pass


class BaseLLMProvider(ABC):
    name: str = "base"
    default_model: str = ""

    def __init__(self, api_key: str | None = None, model: str | None = None) -> None:
        self.api_key = api_key
        self.model = model or self.default_model

    @property
    def is_configured(self) -> bool:
        return bool(self.api_key) or self.name == "mock"

    @abstractmethod
    def complete_json(self, prompt: str, schema_hint: str | None = None) -> dict[str, Any]:
        raise NotImplementedError

    def classify_note(self, title: str, cover_text: str, raw_text: str) -> dict[str, str]:
        prompt = (
            "你是小红书/Rednote 内容策略分析助手。请根据标题、封面文案和正文 OCR 文本，"
            "输出严格 JSON，字段包括 content_type、title_type、cover_type、body_structure、cta_type。"
            "不要输出解释。\n\n"
            f"标题：{title}\n封面文案：{cover_text}\n正文 OCR：{raw_text[:3000]}"
        )
        schema_hint = (
            '{"content_type":"选课决策型","title_type":"问题先行","cover_type":"阶段窗口型",'
            '"body_structure":"立人设 → 讲痛点 → 抛认知 → 引品牌 → 给结果 → 接 CTA",'
            '"cta_type":"评论承接"}'
        )
        data = self.complete_json(prompt, schema_hint=schema_hint)
        return {key: str(data.get(key, "")).strip() for key in ["content_type", "title_type", "cover_type", "body_structure", "cta_type"] if data.get(key)}

    def summarize_competition(self, context: dict[str, Any]) -> dict[str, Any]:
        prompt = (
            "你是品牌内容营销分析师。请基于 Brand A vs Brand B 的结构化样本，输出严格 JSON，"
            "用于竞品种草报告的核心洞察。不要出现真实品牌名。\n\n"
            f"输入：{context}"
        )
        return self.complete_json(prompt)
