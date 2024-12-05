import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.schemas import UserCreate, FileResponse
from app.models import User, File
from app.crud import create_user, get_user_by_email
from app.database import SessionLocal
from datetime import datetime
import os

# Setup FastAPI test client
client = TestClient(app)

@pytest.fixture(scope="module")
def test_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Test Ops User Login
def test_ops_login(test_db):
    user_data = {"email": "opsuser@example.com", "password": "securePassword123"}
    response = client.post("/login", json=user_data)
    assert response.status_code == 200
    assert "access_token" in response.json()

# Test File Upload (Ops User)
def test_ops_upload_file(test_db):
    # Prepare a mock file for upload
    file_data = {"file": ("testfile.pptx", open("testfile.pptx", "rb"), "application/vnd.openxmlformats-officedocument.presentationml.presentation")}
    
    response = client.post("/upload-file", files=file_data)
    assert response.status_code == 200
    assert "message" in response.json() and response.json()["message"] == "file uploaded successfully"

# Test Invalid File Upload (Non-Allowed File Type)
def test_ops_invalid_file_upload(test_db):
    file_data = {"file": ("testfile.txt", open("testfile.txt", "rb"), "text/plain")}
    response = client.post("/upload-file", files=file_data)
    assert response.status_code == 400
    assert "message" in response.json() and response.json()["message"] == "Invalid file type"