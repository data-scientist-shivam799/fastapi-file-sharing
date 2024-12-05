from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.security import hash_password, create_access_token
from app.models import User, File
from app.schemas import UserCreate, FileUpload
from typing import List

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)
    new_user = User(email=user.email, hashed_password=hashed_password, is_ops_user=user.is_ops_user)
    db.add(new_user)
    db.commit()
    return {"message": "User signed up successfully"}

@router.post("/verify-email")
def verify_email(email: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.is_email_verified = True
    db.commit()
    return {"message": "Email verified"}

@router.get("/list-files", response_model=List[FileUpload])
def list_files(db: Session = Depends(get_db)):
    files = db.query(File).all()
    return files
