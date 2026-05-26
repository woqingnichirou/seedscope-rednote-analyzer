from pathlib import Path

from openpyxl import Workbook

from ..models import Note
from .common import ensure_parent


def export_notes_excel(notes: list[Note], path: Path) -> None:
    ensure_parent(path)
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "notes"
    headers = [
        "brand_key",
        "account_name",
        "title",
        "cover_text",
        "likes",
        "collects",
        "comments",
        "published_at",
        "content_type",
        "title_type",
        "cover_type",
        "body_structure",
        "cta_type",
        "body_keywords",
    ]
    sheet.append(headers)
    for note in notes:
        sheet.append([getattr(note, header) for header in headers])
    for column in sheet.columns:
        max_length = max(len(str(cell.value or "")) for cell in column)
        sheet.column_dimensions[column[0].column_letter].width = min(max(max_length + 2, 12), 42)
    workbook.save(path)
