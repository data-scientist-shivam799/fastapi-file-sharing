from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    is_ops_user: Optional[bool] = False

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class FileUpload(BaseModel):
    filename: str
    file_type: str
    uploaded_by: int

class FileResponse(BaseModel):
    id: int
    filename: str
    file_type: str
    uploaded_at: datetime
    uploaded_by: int

    class Config:
        orm_mode = True