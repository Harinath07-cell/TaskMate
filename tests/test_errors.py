def test_get_all_errors(client):
    res = client.get("/api/errors")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    # 8 required error codes
    assert data["count"] == 8
    codes = [e["code"] for e in data["data"]]
    for expected in ["400", "401", "403", "404", "429", "500", "503", "DEV001"]:
        assert expected in codes

def test_get_single_error_dev001(client):
    res = client.get("/api/errors/DEV001")
    assert res.status_code == 200
    data = res.get_json()
    assert data["data"]["code"] == "DEV001"
    assert data["data"]["name"] == "TaskMate Application Error"

def test_error_simulation_endpoints(client):
    # Test all 8 simulated error routes
    assert client.get("/api/errors/test/400").status_code == 400
    assert client.get("/api/errors/test/401").status_code == 401
    assert client.get("/api/errors/test/403").status_code == 403
    assert client.get("/api/errors/test/404").status_code == 404
    assert client.get("/api/errors/test/429").status_code == 429
    assert client.get("/api/errors/test/500").status_code == 500
    assert client.get("/api/errors/test/503").status_code == 503
    assert client.get("/api/errors/test/dev001").status_code == 422

def test_custom_404_html_page(client):
    res = client.get("/nonexistent-page-url", headers={"Accept": "text/html"})
    assert res.status_code == 404
    assert b"Page Not Found" in res.data
    assert b"TaskMate" in res.data
