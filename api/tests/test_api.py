import pytest
from fastapi.testclient import TestClient
from main import *

client = TestClient(app)

def test_get_data():
    action_id = 123
    user_email = "user@ltm.com"
    response = client.get(f"/get_data/{action_id}:{user_email}")
    assert response.status_code == 200
    assert response.json() == {"Action Id": action_id, "Email": user_email}

