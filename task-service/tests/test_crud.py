def test_create_task(client, sample_task):
    resp = client.post("/api/tasks/", json=sample_task)
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "Write tests"
    assert data["user_id"] == 1
    assert data["status"] == "pending"
    assert "id" in data


def test_get_tasks(client, sample_task):
    client.post("/api/tasks/", json=sample_task)
    resp = client.get("/api/tasks/")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1


def test_get_task(client, sample_task):
    created = client.post("/api/tasks/", json=sample_task).json()
    resp = client.get(f"/api/tasks/{created['id']}")
    assert resp.status_code == 200
    assert resp.json()["id"] == created["id"]


def test_get_task_not_found(client):
    resp = client.get("/api/tasks/999")
    assert resp.status_code == 404


def test_update_task(client, sample_task):
    created = client.post("/api/tasks/", json=sample_task).json()
    resp = client.put(f"/api/tasks/{created['id']}", json={"name": "Updated"})
    assert resp.status_code == 200
    assert resp.json()["name"] == "Updated"


def test_update_task_not_found(client):
    resp = client.put("/api/tasks/999", json={"name": "Nope"})
    assert resp.status_code == 404


def test_delete_task(client, sample_task):
    created = client.post("/api/tasks/", json=sample_task).json()
    resp = client.delete(f"/api/tasks/{created['id']}")
    assert resp.status_code == 200
    get_resp = client.get(f"/api/tasks/{created['id']}")
    assert get_resp.status_code == 404


def test_delete_task_not_found(client):
    resp = client.delete("/api/tasks/999")
    assert resp.status_code == 404
