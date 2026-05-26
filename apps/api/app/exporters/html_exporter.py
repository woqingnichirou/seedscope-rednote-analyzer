from pathlib import Path

from .common import ensure_parent


def export_html(html: str, path: Path) -> None:
    ensure_parent(path)
    path.write_text(html, encoding="utf-8")
