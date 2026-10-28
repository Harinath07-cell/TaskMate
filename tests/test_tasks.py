def test_get_tasks_success(client):
    res = client.get("/api/tasks")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert isinstance(data["data"], list)

def test_create_task_success(client):
    payload = {
        "title": "Automated Test Task",
        "description": "Testing create task endpoint",
        "priority": "High",
        "due_date": "2026-11-01"
    }
    res = client.post("/api/tasks", json=payload)
    assert res.status_code == 201
    data = res.get_json()
    assert data["success"] is True
    assert data["data"]["title"] == "Automated Test Task"
    assert data["data"]["priority"] == "High"
    assert data["data"]["is_completed"] is False
    assert "id" in data["data"]

def test_create_task_validation_error(client):
    # Empty title
    res = client.post("/api/tasks", json={"title": "   ", "priority": "High"})
    assert res.status_code == 400
    data = res.get_json()
    assert data["success"] is False
    assert "Task title cannot be empty" in data["error"]["message"]

    # Invalid priority
    res = client.post("/api/tasks", json={"title": "Valid Title", "priority": "Urgent"})
    assert res.status_code == 400
    assert "Priority must be one of" in res.get_json()["error"]["message"]

    # Invalid due date format
    res = client.post("/api/tasks", json={"title": "Valid Title", "due_date": "01-11-2026"})
    assert res.status_code == 400
    assert "Due date must be in YYYY-MM-DD format" in res.get_json()["error"]["message"]

def test_get_single_task(client):
    # Create task first
    create_res = client.post("/api/tasks", json={"title": "Fetch Single Task"})
    task_id = create_res.get_json()["data"]["id"]

    res = client.get(f"/api/tasks/{task_id}")
    assert res.status_code == 200
    assert res.get_json()["data"]["id"] == task_id

def test_get_unknown_task_returns_404(client):
    res = client.get("/api/tasks/999999")
    assert res.status_code == 404
    data = res.get_json()
    assert data["success"] is False
    assert data["error"]["code"] == "404"

def test_update_task(client):
    create_res = client.post("/api/tasks", json={"title": "Pre-update Title", "priority": "Low"})
    task_id = create_res.get_json()["data"]["id"]

    update_payload = {
        "title": "Post-update Title",
        "description": "Added description",
        "priority": "High"
    }
    res = client.put(f"/api/tasks/{task_id}", json=update_payload)
    assert res.status_code == 200
    updated = res.get_json()["data"]
    assert updated["title"] == "Post-update Title"
    assert updated["priority"] == "High"
    assert updated["description"] == "Added description"

def test_complete_and_reopen_task(client):
    create_res = client.post("/api/tasks", json={"title": "Toggle Task"})
    task_id = create_res.get_json()["data"]["id"]

    # Complete
    comp_res = client.patch(f"/api/tasks/{task_id}/complete")
    assert comp_res.status_code == 200
    assert comp_res.get_json()["data"]["is_completed"] is True

    # Reopen
    reopen_res = client.patch(f"/api/tasks/{task_id}/reopen")
    assert reopen_res.status_code == 200
    assert reopen_res.get_json()["data"]["is_completed"] is False

def test_delete_task(client):
    create_res = client.post("/api/tasks", json={"title": "Task to delete"})
    task_id = create_res.get_json()["data"]["id"]

    del_res = client.delete(f"/api/tasks/{task_id}")
    assert del_res.status_code == 200
    assert del_res.get_json()["success"] is True

    # Ensure it no longer exists
    get_res = client.get(f"/api/tasks/{task_id}")
    assert get_res.status_code == 404
