def test_register_login_and_create_task(auth_client, task_client, registered_user):
    token = registered_user["token"]
    headers = {"Authorization": f"Bearer {token}"}

    task_payload = {
        "user_id": 1,
        "name": "Integration task",
        "category": "test",
        "start_time": "2025-06-01T10:00:00",
    }
    resp = task_client.post("/tasks/", json=task_payload, headers=headers)
    assert resp.status_code == 200, f"Create failed: {resp.json()}"
    task = resp.json()
    assert task["name"] == "Integration task"
    assert task["user_id"] == 1
    assert task["status"] == "pending"

    resp = task_client.get("/tasks/", headers=headers)
    assert resp.status_code == 200
    assert len(resp.json()) == 1


def test_task_missing_user_id(auth_client, task_client, registered_user):
    task_payload = {
        "name": "No user_id task",
        "start_time": "2025-06-01T10:00:00",
    }
    resp = task_client.post("/tasks/", json=task_payload)
    assert resp.status_code == 422


def test_complete_task_flow(auth_client, task_client, registered_user):
    token = registered_user["token"]
    headers = {"Authorization": f"Bearer {token}"}

    task = task_client.post(
        "/tasks/",
        json={"user_id": 1, "name": "Complete me", "start_time": "2025-06-01T10:00:00"},
        headers=headers,
    ).json()

    resp = task_client.post(f"/tasks/{task['id']}/complete", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["status"] == "completed"
    assert resp.json()["completed_at"] is not None
