from pathlib import Path
from shutil import copyfileobj

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlmodel import Session, select

from .config import get_settings
from .db import get_session, init_db
from .models import Note, NoteRead, NoteUpdate, Project, ProjectCreate
from .schemas import ExportResponse, ProjectDetail, ReportResponse, UploadResponse
from .services.ocr import ocr_image, parse_note_fields
from .services.reporting import export_project, render_report
from .services.tagger import classify_note_with_provider


app = FastAPI(title="SeedScope API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok", "service": "SeedScope API"}


@app.post("/api/projects", response_model=Project)
def create_project(payload: ProjectCreate, session: Session = Depends(get_session)) -> Project:
    project = Project.model_validate(payload)
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


@app.get("/api/projects", response_model=list[Project])
def list_projects(session: Session = Depends(get_session)) -> list[Project]:
    return session.exec(select(Project).order_by(Project.created_at.desc())).all()


@app.get("/api/projects/{project_id}", response_model=ProjectDetail)
def get_project(project_id: int, session: Session = Depends(get_session)) -> ProjectDetail:
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    notes = session.exec(select(Note).where(Note.project_id == project_id).order_by(Note.created_at.desc())).all()
    return ProjectDetail(project=project, notes=[NoteRead.model_validate(note) for note in notes])


@app.post("/api/projects/{project_id}/uploads/{brand_key}", response_model=UploadResponse)
def upload_images(
    project_id: int,
    brand_key: str,
    files: list[UploadFile] = File(...),
    session: Session = Depends(get_session),
) -> UploadResponse:
    if brand_key not in {"brand_a", "brand_b"}:
        raise HTTPException(status_code=400, detail="brand_key must be brand_a or brand_b")
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    settings = get_settings()
    upload_dir = settings.upload_dir / f"project_{project_id}" / brand_key
    upload_dir.mkdir(parents=True, exist_ok=True)

    created: list[Note] = []
    for file in files:
        safe_name = Path(file.filename or "upload.png").name
        path = upload_dir / safe_name
        with path.open("wb") as output:
            copyfileobj(file.file, output)
        raw_text = ocr_image(path)
        fields = parse_note_fields(raw_text, path.stem)
        tags = classify_note_with_provider(fields["title"], fields["cover_text"], raw_text)
        note = Note(project_id=project_id, brand_key=brand_key, image_path=str(path), **fields, **tags)
        session.add(note)
        created.append(note)

    session.commit()
    for note in created:
        session.refresh(note)
    return UploadResponse(notes=[NoteRead.model_validate(note) for note in created])


@app.put("/api/notes/{note_id}", response_model=NoteRead)
def update_note(note_id: int, payload: NoteUpdate, session: Session = Depends(get_session)) -> Note:
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(note, key, value)
    session.add(note)
    session.commit()
    session.refresh(note)
    return note


@app.post("/api/projects/{project_id}/tag", response_model=list[NoteRead])
def tag_project(project_id: int, session: Session = Depends(get_session)) -> list[Note]:
    notes = session.exec(select(Note).where(Note.project_id == project_id)).all()
    for note in notes:
        tags = classify_note_with_provider(note.title, note.cover_text, note.raw_ocr_text)
        for key, value in tags.items():
            setattr(note, key, value)
        session.add(note)
    session.commit()
    return session.exec(select(Note).where(Note.project_id == project_id)).all()


@app.post("/api/projects/{project_id}/report", response_model=ReportResponse)
def generate_report(project_id: int, session: Session = Depends(get_session)) -> ReportResponse:
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    notes = session.exec(select(Note).where(Note.project_id == project_id)).all()
    report = render_report(session, project, notes)
    return ReportResponse(report_id=report.id or 0, markdown=report.markdown, html=report.html)


@app.post("/api/projects/{project_id}/exports", response_model=ExportResponse)
def create_exports(project_id: int, session: Session = Depends(get_session)) -> ExportResponse:
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return ExportResponse(**export_project(session, project))


@app.get("/api/exports/{project_dir}/{filename}")
def get_export(project_dir: str, filename: str) -> FileResponse:
    settings = get_settings()
    path = settings.export_dir / project_dir / filename
    if not path.exists():
        raise HTTPException(status_code=404, detail="Export not found")
    return FileResponse(path)
