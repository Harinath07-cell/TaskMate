def test_health_endpoint(client):
    res = client.get("/health")
    # Health status should be 200 since database is connected
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] in ("healthy", "degraded")
    assert "dependencies" in data
    assert "database" in data["dependencies"]
    assert data["dependencies"]["database"]["status"] == "connected"
    assert "mongodb" in data["dependencies"]
    assert "ai_assistant" in data["dependencies"]

def test_joke_endpoint(client):
    res = client.get("/api/joke")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "setup" in data["data"]
    assert "punchline" in data["data"]
    assert data["data"]["source"] in ("official-joke-api", "fallback")
