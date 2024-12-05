from fastapi import APIRouter, HTTPException, Depends, UploadFile
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.security import hash_password
from app.models import User, File
from app.schemas import UserLogin, FileUpload
from typing import List

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
def ops_login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not db_user.is_ops_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Logged in as Ops User"}

@router.post("/upload-file")
def upload_file(file: UploadFile, db: Session = Depends(get_db)):
    if file.content_type not in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                 "application/vnd.openxmlformats-officedocument.presentationml.presentation",
                                 "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]:
        raise HTTPException(status_code=400, detail="File type not allowed")
    new_file = File(filename=file.filename, file_type=file.content_type, uploaded_by_id=1)  # Replace with actual user ID
    db.add(new_file)
    db.commit()
    return {"message": "File uploaded successfully"}
