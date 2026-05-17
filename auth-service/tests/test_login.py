def test_login_ok(client, test_user_data):
    client.post("/api/register", json=test_user_data)
    resp = client.post("/api/login", json={"username": "testuser", "password": "secure123"})
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, test_user_data):
    client.post("/api/register", json=test_user_data)
    resp = client.post("/api/login", json={"username": "testuser", "password": "wrongpass"})
    assert resp.status_code == 401
    assert "Invalid credentials" in resp.json()["detail"]


def test_login_nonexistent(client):
    resp = client.post("/api/login", json={"username": "ghost", "password": "x"})
    assert resp.status_code == 401


def test_login_missing_fields(client):
    resp = client.post("/api/login", json={"username": "x"})
    assert resp.status_code == 422
