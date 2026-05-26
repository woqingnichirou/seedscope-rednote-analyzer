import re
from pathlib import Path

from PIL import Image


def _run_paddleocr(path: Path) -> str | None:
    try:
        from paddleocr import PaddleOCR  # type: ignore

        engine = PaddleOCR(use_angle_cls=True, lang="ch", show_log=False)
        result = engine.ocr(str(path), cls=True)
        lines: list[str] = []
        for page in result or []:
            for item in page or []:
                if len(item) > 1 and item[1]:
                    lines.append(str(item[1][0]))
        return "\n".join(lines).strip()
    except Exception:
        return None


def _run_tesseract(path: Path) -> str | None:
    try:
        import pytesseract

        image = Image.open(path)
        return pytesseract.image_to_string(image, lang="chi_sim+eng").strip()
    except Exception:
        return None


def ocr_image(path: Path) -> str:
    text = _run_paddleocr(path) or _run_tesseract(path)
    if text:
        return text
    return f"未识别图片文本。文件名：{path.stem}"


def parse_note_fields(raw_text: str, filename: str) -> dict:
    text = raw_text.replace("\r", "\n")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    compact = " ".join(lines)

    def number_after(patterns: list[str]) -> int:
        for pattern in patterns:
            match = re.search(pattern, compact, re.IGNORECASE)
            if match:
                value = match.group(1).replace(",", "")
                try:
                    if value.lower().endswith("k"):
                        return int(float(value[:-1]) * 1000)
                    if "万" in value:
                        return int(float(value.replace("万", "")) * 10000)
                    return int(float(value))
                except ValueError:
                    continue
        return 0

    title = lines[0] if lines else filename
    cover_text = " / ".join(lines[:3]) if lines else filename
    account = ""
    for line in lines:
        if any(key in line.lower() for key in ["@", "账号", "author", "博主"]):
            account = line.replace("账号", "").replace("博主", "").replace("：", "").strip()
            break

    published = ""
    date_match = re.search(r"(20\d{2}[-/.年]\d{1,2}[-/.月]\d{1,2}日?)", compact)
    if date_match:
        published = date_match.group(1)

    return {
        "account_name": account,
        "title": title[:120],
        "cover_text": cover_text[:240],
        "body_keywords": extract_keywords(compact),
        "likes": number_after([r"(?:点赞|赞|likes?)[:： ]*([\d,.]+万?|[\d.]+k)", r"([\d,.]+万?|[\d.]+k)\s*(?:点赞|赞)"]),
        "collects": number_after([r"(?:收藏|collects?)[:： ]*([\d,.]+万?|[\d.]+k)", r"([\d,.]+万?|[\d.]+k)\s*收藏"]),
        "comments": number_after([r"(?:评论|comments?)[:： ]*([\d,.]+万?|[\d.]+k)", r"([\d,.]+万?|[\d.]+k)\s*评论"]),
        "published_at": published,
        "raw_ocr_text": raw_text,
    }


def extract_keywords(text: str) -> str:
    candidates = [
        "避坑",
        "对比",
        "攻略",
        "测评",
        "阶段",
        "体验",
        "试听",
        "价格",
        "外教",
        "口语",
        "效果",
        "方法",
        "真实",
        "孩子",
        "家长",
    ]
    hits = [word for word in candidates if word in text]
    return "、".join(hits[:8])
