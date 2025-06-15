import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



from fastapi.testclient import TestClient
from api.app import app


client = TestClient(app)

def test_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Job Role Recommendation API"}

def test_available_skills():
    response = client.get("/available_skills")
    assert response.status_code == 200
    data = response.json()
    assert "skills" in data
    assert isinstance(data["skills"], list)
    assert len(data["skills"]) >= 15
    assert all(isinstance(skill, str) for skill in data["skills"])

def test_recommend_valid_input():
    payload = {
        "skills": ["python", "machine learning"],
        "experience": 3
    }
    response = client.post("/recommend", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "recommendations" in data
    assert isinstance(data["recommendations"], list)
    assert len(data["recommendations"]) == 5

def test_recommend_missing_skills():
    payload = {
        "experience": 3
    }
    response = client.post("/recommend", json=payload)
    assert response.status_code == 422  # Unprocessable Entity (validation error)

def test_recommend_empty_skills():
    payload = {
        "skills": [],
        "experience": 3
    }
    response = client.post("/recommend", json=payload)
    assert response.status_code == 422  # Unprocessable Entity (validation error)