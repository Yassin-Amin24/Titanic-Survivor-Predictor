# import os
# import json
# import pytest
# import sqlite3
# from fastapi.testclient import TestClient
# from unittest.mock import patch

# # Import from your backend
# from main import app, init_database, hash_password

# client = TestClient(app)

# # Use a test-specific DB to avoid messing with production
# TEST_DB = "test_titanic_app.db"

# @pytest.fixture(scope="module", autouse=True)
# def setup_and_teardown():
#     # Monkey patch sqlite to use test DB
#     original_connect = sqlite3.connect

#     def test_connect(db_name=TEST_DB, *args, **kwargs):
#         return original_connect(TEST_DB, *args, **kwargs)

#     sqlite3.connect = test_connect

#     if os.path.exists(TEST_DB):
#         os.remove(TEST_DB)
#     init_database()
#     yield

#     if os.path.exists(TEST_DB):
#         os.remove(TEST_DB)
#     sqlite3.connect = original_connect

# def test_password_hashing():
#     pw = "mysecretpassword"
#     hashed = hash_password(pw)
#     assert hashed == hash_password(pw)
#     assert hashed != hash_password("otherpass")

# def test_register_user():
#     res = client.post("/api/auth/register", json={
#         "email": "testuser@example.com",
#         "password": "test123"
#     })
#     assert res.status_code == 200
#     assert "token" in res.json()
#     assert res.json()["user"]["email"] == "testuser@example.com"

# def test_login_user():
#     res = client.post("/api/auth/login", json={
#         "email": "testuser@example.com",
#         "password": "test123"
#     })
#     assert res.status_code == 200
#     assert "token" in res.json()

# def test_get_current_user():
#     login = client.post("/api/auth/login", json={
#         "email": "testuser@example.com",
#         "password": "test123"
#     })
#     token = login.json()["token"]
#     res = client.get("/api/auth/me", headers={
#         "Authorization": f"Bearer {token}"
#     })
#     assert res.status_code == 200
#     assert res.json()["user"]["email"] == "testuser@example.com"

# mock_prediction_response = {
#     "predictions": {
#         "RandomForest": {"survived": True, "probability": 0.95}
#     }
# }

# @patch("main.requests.post")
# def test_predict_with_mock(mock_post):
#     mock_post.return_value.status_code = 200
#     mock_post.return_value.json.return_value = mock_prediction_response

#     login = client.post("/api/auth/login", json={
#         "email": "testuser@example.com",
#         "password": "test123"
#     })
#     token = login.json()["token"]

#     res = client.post("/api/predict", json={
#         "passenger": {
#             "pclass": 1,
#             "sex": "female",
#             "age": 28,
#             "fare": 90.0,
#             "traveled_alone": True,
#             "embarked": "S",
#             "title": "Miss"
#         },
#         "model_names": ["RandomForest"]
#     }, headers={"Authorization": f"Bearer {token}"})

#     assert res.status_code == 200
#     assert "predictions" in res.json()

# def test_health_check():
#     res = client.get("/health")
#     assert res.status_code == 200
#     assert res.json()["status"] == "healthy"

import os
import json
import pytest
import sqlite3
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app, init_database, hash_password, get_current_user



client = TestClient(app)
TEST_DB = "test_titanic_app.db"

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    # Force sqlite3 to use test DB
    original_connect = sqlite3.connect
    def test_connect(db_name=TEST_DB, *args, **kwargs):
        return original_connect(TEST_DB, *args, **kwargs)
    sqlite3.connect = test_connect

    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    init_database()
    yield
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    sqlite3.connect = original_connect

def test_password_hashing():
    pw = "mysecretpassword"
    hashed = hash_password(pw)
    assert hashed == hash_password(pw)
    assert hashed != hash_password("wrongpass")

def test_register_user():
    res = client.post("/api/auth/register", json={
        "email": "testuser@example.com",
        "password": "test123"
    })
    assert res.status_code == 200
    assert "token" in res.json()

def test_login_user():
    res = client.post("/api/auth/login", json={
        "email": "testuser@example.com",
        "password": "test123"
    })
    assert res.status_code == 200
    assert "token" in res.json()

def test_get_current_user():
    login = client.post("/api/auth/login", json={
        "email": "testuser@example.com",
        "password": "test123"
    })
    token = login.json()["token"]
    res = client.get("/api/auth/me", headers={
        "Authorization": f"Bearer {token}"
    })
    assert res.status_code == 200
    assert res.json()["user"]["email"] == "testuser@example.com"

@patch("main.requests.post")
def test_predict_with_mock(mock_post):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "predictions": {
            "RandomForest": {"survived": True, "probability": 0.95}
        }
    }

    # Override dependency to simulate a logged-in user
    app.dependency_overrides[get_current_user] = lambda: {
        "id": 1,
        "email": "testuser@example.com",
        "is_admin": False,
        "created_at": "2025-01-01T00:00:00"
    }

    res = client.post("/api/predict", json={
        "request": {  # 💥 Wrap inside "request" key
            "passenger": {
                "pclass": 1,
                "sex": "female",
                "age": 28,
                "fare": 90.0,
                "traveled_alone": True,
                "embarked": "S",
                "title": "Miss"
            },
            "model_names": ["RandomForest"]
        }
    })

    print(res.text)  # Helps debugging if test fails
    assert res.status_code == 200
    assert "predictions" in res.json()


def test_health_check():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"
