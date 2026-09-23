from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_profile_endpoint():
    files = {"file": ("students.csv", b"Name,Score\nAli,80\nSara,90\n", "text/csv")}
    response = client.post("/datasets/profile", files=files)
    assert response.status_code == 200
    assert response.json()["profile"]["shape"]["rows"] == 2

def test_reject_invalid_file():
    files = {"file": ("students.txt", b"hello", "text/plain")}
    response = client.post("/datasets/profile", files=files)
    assert response.status_code == 400
