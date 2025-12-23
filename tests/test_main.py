from fastapi.testclient import TestClient

import app.main as main

client = TestClient(main.app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Recipe Storage API Running"}
