def test_get_faqs(client):
    res = client.get("/api/faqs")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    # At least 10 FAQs required by specification (we seeded 12)
    assert data["count"] >= 10
    first = data["data"][0]
    assert "question" in first
    assert "answer" in first

def test_search_faqs_matching(client):
    res = client.get("/api/faqs/search?q=TaskMate")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert data["count"] > 0
    assert any("TaskMate" in item["question"] or "TaskMate" in item["answer"] for item in data["data"])

def test_search_faqs_empty_query(client):
    res = client.get("/api/faqs/search?q=")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert data["count"] >= 10

def test_get_single_faq(client):
    res = client.get("/api/faqs/1")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert data["data"]["id"] == 1

def test_get_unknown_faq_returns_404(client):
    res = client.get("/api/faqs/99999")
    assert res.status_code == 404
    data = res.get_json()
    assert data["success"] is False
    assert data["error"]["code"] == "404"
