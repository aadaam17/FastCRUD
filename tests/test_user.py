# pytest -s: show print
# pytest -x: stop test on first failed test, instead of continue test others
# pytest --disable-warnings: disable warnings

import pytest
from app import schemas
from jose import jwt
from app.config import settings

# def test_root(client):
#     res = client.get("/")
#     result = res.json().get("message")
#     print(result)
#     assert result == "Welcome to the API"

def test_create_user(client):
    res = client.post("/users/", json={"email": "maan@gmail.com", "password": "password123"})
    
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "maan@gmail.com"
    assert res.status_code == 201
    
    
def test_login_user(test_user, client):
    res = client.post("/login", data={"username": test_user["email"], "password": test_user["password"]})
    print(res.json())
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ("tester0@gmail.com", "wrongpassword", 403),
    ("wrongemail@gmail.com", "password123", 403),
    ("wrongemail@gmail.com", "wrongpassword", 403),
    (None, "password123", 403),
    ("tester0@gmail.com", None, 403),
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    
    # print(res.json())
    print(res.status_code)
    assert res.status_code == status_code
    assert res.json().get("detail") == "Invalid Credentials"