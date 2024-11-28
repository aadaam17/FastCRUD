from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    res = client.get("/")
    result = res.json().get("message")
    print(result)
    assert result == "Welcome to the API"