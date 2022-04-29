from fastapi.testclient import TestClient
from app.main import app

print(type(app))
client = TestClient(app)

def test_root():
    res = client.get('/')
    print(res)