def test_complete_task(client, sample_task):
    created = client.post("/api/tasks/", json=sample_task).json()
    task_id = created["id"]
    resp = client.post(f"/api/tasks/{task_id}/complete")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "completed"
    assert data["completed_at"] is not None


def test_complete_task_not_found(client):
    resp = client.post("/api/tasks/999/complete")
    assert resp.status_code == 404
