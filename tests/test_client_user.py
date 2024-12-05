import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.schemas import UserCreate, FileResponse
from app.models import User
from app.crud import create_user, get_user_by_email
from app.database import SessionLocal
from datetime import datetime

# Setup FastAPI test client
client = TestClient(app)

@pytest.fixture(scope="module")
def test_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Test Signup
def test_client_signup(test_db):
    user_data = {"email": "client@example.com", "password": "securePassword123", "user_type": "client"}
    response = client.post("/signup", json=user_data)
    assert response.status_code == 200
    assert "verification_url" in response.json()

# Test Login
def test_client_login(test_db):
    user_data = {"email": "client@example.com", "password": "securePassword123"}
    response = client.post("/login", json=user_data)
    assert response.status_code == 200
    assert "access_token" in response.json()

# Test List Files (Client User)
def test_list_files(test_db):
    response = client.get("/list-files")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Ensuring the response is a list

# Test Download File (Client User)
def test_download_file(test_db):
    # Assuming we have a valid assignment ID for a file
    assignment_id = "validAssignmentId"
    response = client.get(f"/download-file/{assignment_id}")
    assert response.status_code == 200
    assert "download-link" in response.json()
    assert "message" in response.json()