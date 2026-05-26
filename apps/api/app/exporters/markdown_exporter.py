from pathlib import Path

from .common import ensure_parent


def export_markdown(markdown: str, path: Path) -> None:
    ensure_parent(path)
    path.write_text(markdown, encoding="utf-8")
