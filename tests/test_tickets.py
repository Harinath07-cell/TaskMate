import re

def test_create_ticket_success(client):
    payload = {
        "title": "Cannot sync tasks",
        "description": "Encountering intermittent connection errors when saving tasks.",
        "email": "student@kct.ac.in"
    }
    res = client.post("/api/tickets", json=payload)
    assert res.status_code == 201
    data = res.get_json()
    assert data["success"] is True
    ticket_code = data["data"]["ticket_code"]
    assert re.match(r"^TKT-\d{4}-[A-Z0-9]{4}$", ticket_code)
    assert data["data"]["status"] == "OPEN"

def test_create_ticket_without_email(client):
    payload = {
        "title": "Question on priority",
        "description": "How do priority weights work?"
    }
    res = client.post("/api/tickets", json=payload)
    assert res.status_code == 201
    assert res.get_json()["data"]["email_notified"] is False

def test_create_ticket_validation_error(client):
    # Missing title
    res = client.post("/api/tickets", json={"description": "Missing title"})
    assert res.status_code == 400

    # Missing description
    res = client.post("/api/tickets", json={"title": "Missing description"})
    assert res.status_code == 400

    # Invalid email
    res = client.post("/api/tickets", json={"title": "Title", "description": "Desc", "email": "invalid-email"})
    assert res.status_code == 400
    assert "Invalid email address" in res.get_json()["error"]["message"]

def test_get_ticket_status(client):
    # Create ticket
    create_res = client.post("/api/tickets", json={
        "title": "Check status ticket",
        "description": "Need to track status"
    })
    ticket_code = create_res.get_json()["data"]["ticket_code"]

    res = client.get(f"/api/tickets/{ticket_code}")
    assert res.status_code == 200
    ticket = res.get_json()["data"]
    assert ticket["ticket_code"] == ticket_code
    assert ticket["status"] == "OPEN"

def test_get_unknown_ticket_returns_404(client):
    res = client.get("/api/tickets/TKT-9999-XXXX")
    assert res.status_code == 404
