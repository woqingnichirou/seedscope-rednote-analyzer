from pydantic import BaseModel

from .models import NoteRead, Project


class ProjectDetail(BaseModel):
    project: Project
    notes: list[NoteRead]


class UploadResponse(BaseModel):
    notes: list[NoteRead]


class ReportResponse(BaseModel):
    report_id: int
    markdown: str
    html: str


class ExportResponse(BaseModel):
    markdown_url: str
    html_url: str
    excel_url: str
