def test_register_ok(client, test_user_data):
    resp = client.post("/register", json=test_user_data)
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_register_duplicate_username(client, test_user_data):
    client.post("/register", json=test_user_data)
    resp = client.post("/register", json=test_user_data)
    assert resp.status_code == 409
    assert "Username already taken" in resp.json()["detail"]


def test_register_duplicate_email(client, test_user_data):
    client.post("/register", json=test_user_data)
    dup = {"username": "other", "email": "test@example.com", "password": "secure123"}
    resp = client.post("/register", json=dup)
    assert resp.status_code == 409
    assert "Email already registered" in resp.json()["detail"]


def test_register_missing_fields(client):
    resp = client.post("/register", json={"username": "foo"})
    assert resp.status_code == 422
