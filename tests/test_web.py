import pytest
from fastapi.testclient import TestClient
from krane.web.app import app

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint returns correct response"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome to Krane API" in response.json()["message"]

def test_analyze_sequence():
    """Test sequence analysis endpoint"""
    payload = {
        "sequence": "ATCG",
        "sequence_type": "DNA",
        "label": "Test Sequence"
    }
    response = client.post("/api/sequence/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["sequence"] == "ATCG"
    assert data["sequence_type"] == "DNA"
    assert len(data["sequence"]) == 4

def test_generate_sequence():
    """Test sequence generation endpoint"""
    payload = {
        "length": 10,
        "sequence_type": "DNA"
    }
    response = client.post("/api/sequence/generate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert len(data["sequence"]) == 10
    assert all(base in "ATCG" for base in data["sequence"])

def test_transcribe_sequence():
    """Test transcription endpoint"""
    payload = {
        "sequence": "ATCG",
        "sequence_type": "DNA",
        "label": "Test"
    }
    response = client.post("/api/sequence/transcribe", json=payload)
    assert response.status_code == 200
    assert response.json()["transcribed_sequence"] == "AUCG"

def test_invalid_sequence():
    """Test handling of invalid sequence"""
    payload = {
        "sequence": "ATCGX",  # Invalid nucleotide
        "sequence_type": "DNA",
        "label": "Test"
    }
    response = client.post("/api/sequence/analyze", json=payload)
    assert response.status_code == 400

def test_proteins():
    """Test protein finding endpoint"""
    payload = {
        "sequence": "ATGGCCTAA",  # Start-Ala-Stop
        "sequence_type": "DNA",
        "label": "Test"
    }
    response = client.post("/api/sequence/proteins", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "MA" in data["proteins"]

@pytest.mark.parametrize("endpoint", [
    "/api/sequence/analyze",
    "/api/sequence/transcribe",
    "/api/sequence/proteins"
])
def test_missing_required_fields(endpoint):
    """Test handling of missing required fields"""
    response = client.post(endpoint, json={})
    assert response.status_code == 422