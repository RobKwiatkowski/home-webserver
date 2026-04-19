from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from fastapi.responses import FileResponse as FastAPIFileResponse
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import FileRecord
from ..schemas import FileResponse

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

ALLOWED_CONTENT_TYPES = {
    "image/jpeg",
    "image/png",
    "application/pdf",
    "text/plain",
}

router = APIRouter(prefix="/files", tags=["files"])

UPLOAD_DIR = Path("/app/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.get("", response_model=list[FileResponse])
def list_files(db: Session = Depends(get_db)):
    return db.query(FileRecord).order_by(FileRecord.created_at.desc()).all()


@router.post("", response_model=FileResponse)
def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Brakuje nazwy pliku.")

    stored_name = f"{uuid4()}_{file.filename}"
    file_path = UPLOAD_DIR / stored_name

    content = file.file.read()
    file_size = len(content)
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="Plik jest za duży. Maksymalny rozmiar to 5 MB.")
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Nieobsługiwany typ pliku."
        )

    with open(file_path, "wb") as f:
        f.write(content)

    db_file = FileRecord(
        original_name=file.filename,
        stored_name=stored_name,
        content_type=file.content_type,
        size=file_size,
    )

    db.add(db_file)
    db.commit()
    db.refresh(db_file)

    return db_file


@router.get("/{file_id}", response_model=FileResponse)
def get_file(file_id: int, db: Session = Depends(get_db)):
    db_file = db.query(FileRecord).filter(FileRecord.id == file_id).first()

    if db_file is None:
        raise HTTPException(status_code=404, detail="Nie znaleziono pliku na dysku.")

    return db_file


@router.get("/{file_id}/download")
def download_file(file_id: int, db: Session = Depends(get_db)):
    db_file = db.query(FileRecord).filter(FileRecord.id == file_id).first()

    if db_file is None:
        raise HTTPException(status_code=404, detail="Nie znaleziono pliku na dysku.")

    file_path = UPLOAD_DIR / db_file.stored_name

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Stored file not found")

    return FastAPIFileResponse(
        path=file_path,
        filename=db_file.original_name,
        media_type=db_file.content_type or "application/octet-stream",
    )

@router.delete("/{file_id}")
def delete_file(file_id: int, db: Session = Depends(get_db)):
    db_file = db.query(FileRecord).filter(FileRecord.id == file_id).first()

    if db_file is None:
        raise HTTPException(status_code=404, detail="Nie znaleziono pliku na dysku.")

    file_path = UPLOAD_DIR / db_file.stored_name

    if file_path.exists():
        file_path.unlink()

    db.delete(db_file)
    db.commit()

    return {"message": "File deleted successfully"}