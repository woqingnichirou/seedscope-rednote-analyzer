from collections import Counter
from datetime import datetime
from pathlib import Path
import re

from ..models import Note, Project


def safe_filename_part(value: str) -> str:
    cleaned = re.sub(r'[\\/:*?"<>|]+', "_", value).strip()
    return cleaned or "demo_project"


def today_compact() -> str:
    return datetime.now().strftime("%Y%m%d")


def report_project_name(project: Project) -> str:
    return safe_filename_part(f"{project.brand_a}_vs_{project.brand_b}")


def word_filename(project: Project) -> str:
    return f"SeedScope_竞品分析报告_{report_project_name(project)}_{today_compact()}.docx"


def ppt_filename(project: Project) -> str:
    return f"SeedScope_竞品分析报告_{report_project_name(project)}_{today_compact()}.pptx"


def split_notes(notes: list[Note]) -> tuple[list[Note], list[Note]]:
    return [n for n in notes if n.brand_key == "brand_a"], [n for n in notes if n.brand_key == "brand_b"]


def avg(notes: list[Note], field: str) -> float:
    if not notes:
        return 0
    return sum(getattr(note, field) for note in notes) / len(notes)


def top_counter(notes: list[Note], field: str, limit: int = 5) -> list[tuple[str, int]]:
    counter = Counter(getattr(note, field) or "未分类" for note in notes)
    return counter.most_common(limit)


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
