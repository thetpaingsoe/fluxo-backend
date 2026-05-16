def test_auth_health(auth_client):
    resp = auth_client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "healthy"


def test_task_health(task_client):
    resp = task_client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "healthy"


def test_register_returns_token(auth_client):
    resp = auth_client.post("/register", json={
        "username": "newuser",
        "email": "new@test.com",
        "password": "mypass",
    })
    assert resp.status_code == 200
    assert "access_token" in resp.json()


def test_login_returns_token(auth_client):
    auth_client.post("/register", json={
        "username": "loginuser",
        "email": "login@test.com",
        "password": "mypass",
    })
    resp = auth_client.post("/login", json={
        "username": "loginuser",
        "password": "mypass",
    })
    assert resp.status_code == 200
    assert "access_token" in resp.json()
