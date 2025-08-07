import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Titanic Model Backend API" in response.json().get("message", "")

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json().get("status") == "healthy"

def test_get_features():
    response = client.get("/api/features")
    assert response.status_code == 200
    assert "features" in response.json()
    
