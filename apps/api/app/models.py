from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class ProjectBase(SQLModel):
    brand_a: str = "Brand A"
    brand_b: str = "Brand B"
    industry: str
    period: str
    objective: str


class Project(ProjectBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ProjectCreate(ProjectBase):
    pass


class NoteBase(SQLModel):
    project_id: int = Field(foreign_key="project.id")
    brand_key: str
    image_path: str
    account_name: str = ""
    title: str = ""
    cover_text: str = ""
    body_keywords: str = ""
    likes: int = 0
    collects: int = 0
    comments: int = 0
    published_at: str = ""
    content_type: str = ""
    title_type: str = ""
    cover_type: str = ""
    body_structure: str = ""
    cta_type: str = ""
    raw_ocr_text: str = ""


class Note(NoteBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class NoteRead(NoteBase):
    id: int
    created_at: datetime


class NoteUpdate(SQLModel):
    account_name: str | None = None
    title: str | None = None
    cover_text: str | None = None
    body_keywords: str | None = None
    likes: int | None = None
    collects: int | None = None
    comments: int | None = None
    published_at: str | None = None
    content_type: str | None = None
    title_type: str | None = None
    cover_type: str | None = None
    body_structure: str | None = None
    cta_type: str | None = None


class Report(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id")
    markdown: str
    html: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
