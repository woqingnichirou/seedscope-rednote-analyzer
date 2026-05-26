from ..llm.factory import get_llm_provider


TAG_FIELDS = ["content_type", "title_type", "cover_type", "body_structure", "cta_type"]


def classify_note_with_provider(title: str, cover_text: str, raw_text: str) -> dict[str, str]:
    rule_tags = classify_note(title, cover_text, raw_text)
    provider = get_llm_provider()
    if not provider.is_configured:
        return rule_tags

    try:
        llm_tags = provider.classify_note(title, cover_text, raw_text)
    except Exception:
        return rule_tags

    merged = rule_tags.copy()
    for key in TAG_FIELDS:
        if llm_tags.get(key):
            merged[key] = llm_tags[key]
    return merged


def classify_note(title: str, cover_text: str, raw_text: str) -> dict[str, str]:
    text = f"{title} {cover_text} {raw_text}"
    return {
        "content_type": classify_content_type(text),
        "title_type": classify_title_type(title),
        "cover_type": classify_cover_type(cover_text),
        "body_structure": classify_body_structure(text),
        "cta_type": classify_cta(text),
    }


def classify_content_type(text: str) -> str:
    if any(key in text for key in ["对比", "哪家", "测评", "横评"]):
        return "横向对比"
    if any(key in text for key in ["避坑", "怎么买", "怎么选", "选课"]):
        return "选课避坑"
    if any(key in text for key in ["从不", "变化", "提升", "敢说", "结果"]):
        return "结果反差"
    if any(key in text for key in ["方法", "攻略", "清单", "步骤"]):
        return "方法攻略"
    if any(key in text for key in ["一年级", "二年级", "8岁", "低龄", "阶段"]):
        return "阶段窗口"
    return "真实体验"


def classify_title_type(title: str) -> str:
    if any(key in title for key in ["哪家", "对比", "测评", "vs"]):
        return "对比型"
    if any(key in title for key in ["怎么", "如何", "攻略", "方法", "避坑"]):
        return "方法型"
    if any(key in title for key in ["为什么", "怎么办", "问题"]):
        return "问题型"
    if any(key in title for key in ["提升", "变化", "结果", "敢说"]):
        return "结果型"
    if any(key in title.lower() for key in ["brand", "官方", "推荐"]):
        return "品牌直露型"
    return "经验型"


def classify_cover_type(cover_text: str) -> str:
    if any(key in cover_text for key in ["一年级", "二年级", "岁", "阶段"]):
        return "阶段窗口型"
    if any(key in cover_text for key in ["前后", "变化", "提升", "不敢说"]):
        return "结果反差型"
    if any(key in cover_text for key in ["避坑", "别踩", "怎么选"]):
        return "选课避坑型"
    if any(key in cover_text for key in ["实拍", "记录", "反馈", "截图"]):
        return "证据陪跑型"
    return "信息摘要型"


def classify_body_structure(text: str) -> str:
    steps = []
    if any(key in text for key in ["我是", "妈妈", "家长", "过来人"]):
        steps.append("立人设")
    if any(key in text for key in ["痛点", "不会", "不敢", "发音", "困难"]):
        steps.append("讲痛点")
    if any(key in text for key in ["标准", "判断", "方法", "框架"]):
        steps.append("抛认知")
    if any(key in text.lower() for key in ["brand a", "brand b", "课程", "产品"]):
        steps.append("引品牌")
    if any(key in text for key in ["结果", "提升", "变化", "反馈"]):
        steps.append("给结果")
    return " → ".join(steps) if steps else "体验 → 卖点 → 推荐"


def classify_cta(text: str) -> str:
    if any(key in text for key in ["评论", "留言"]):
        return "评论承接"
    if any(key in text for key in ["私信", "关键词"]):
        return "私信承接"
    if any(key in text for key in ["试听", "领取", "资料", "链接"]):
        return "试听/资料承接"
    if any(key in text for key in ["进群", "社群"]):
        return "社群承接"
    return "弱 CTA"
