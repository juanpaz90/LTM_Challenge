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


def test_read_app_info():
    app_id = 321
    app_department = "LTM_dept"
    response = client.get(f"/app_info/{app_id}:{app_department}")
    assert response.status_code == 401  # Expecting authentication error
    assert response.json() == {"detail": "You have to authenticate in your company portal"}
