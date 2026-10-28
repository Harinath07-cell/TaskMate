def test_chat_empty_message(client):
    res = client.post("/api/chat", json={"message": ""})
    assert res.status_code == 400
    assert "Message text cannot be empty" in res.get_json()["error"]["message"]

def test_chat_oversized_message(client):
    oversized = "a" * 501
    res = client.post("/api/chat", json={"message": oversized})
    assert res.status_code == 400
    assert "500 characters" in res.get_json()["error"]["message"]

def test_chat_faq_grounded_answer(client):
    res = client.post("/api/chat", json={"message": "What is TaskMate?"})
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "TaskMate" in data["data"]["response"]
    assert "conversation_id" in data["data"]
    assert "message_id" in data["data"]

def test_chat_error_explanation_grounded(client):
    res = client.post("/api/chat", json={"message": "Explain error 404"})
    assert res.status_code == 200
    data = res.get_json()
    assert "Not Found" in data["data"]["response"]

def test_chat_dev001_explanation_grounded(client):
    res = client.post("/api/chat", json={"message": "What is error DEV001?"})
    assert res.status_code == 200
    data = res.get_json()
    assert "DEV001" in data["data"]["response"]
    assert "TaskMate Application Error" in data["data"]["response"]

def test_chat_unresolved_offers_ticket(client):
    res = client.post("/api/chat", json={"message": "xyzquantumxyzunknownproblem12345"})
    assert res.status_code == 200
    data = res.get_json()
    assert data["data"]["suggest_ticket"] is True
    assert "support ticket" in data["data"]["response"].lower()

def test_chat_feedback(client):
    res = client.post("/api/chat/feedback", json={
        "conversation_id": "test_conv",
        "message_id": "test_msg",
        "rating": "helpful",
        "comment": "Very clear response!"
    })
    assert res.status_code == 200
    assert res.get_json()["success"] is True

def test_chat_rate_limiting(client):
    # Send requests to trigger rate limit (configured to 30)
    triggered = False
    for i in range(35):
        res = client.post("/api/chat", json={"message": f"ping {i}"}, environ_base={"REMOTE_ADDR": "192.168.1.100"})
        if res.status_code == 429:
            triggered = True
            break
    assert triggered is True

def test_groq_api_call_mocked(client, monkeypatch):
    from unittest.mock import MagicMock
    import requests
    from backend.config import Config

    monkeypatch.setattr(Config, "GROQ_API_KEY", "gsk_test_fake_key_123")
    monkeypatch.setattr(Config, "GROQ_MODEL", "llama-3.3-70b-versatile")

    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "choices": [
            {
                "message": {
                    "content": "Hello from Groq LPU with Llama 3.3!"
                }
            }
        ]
    }

    with monkeypatch.context() as m:
        m.setattr(requests, "post", lambda url, **kwargs: mock_resp)
        res = client.post("/api/chat", json={"message": "Tell me about productivity"})
        assert res.status_code == 200
        data = res.get_json()
        assert data["success"] is True
        assert data["data"]["source"] == "groq"
        assert "Hello from Groq LPU with Llama 3.3!" in data["data"]["response"]

def test_groq_api_tool_calling_mocked(client, monkeypatch):
    from unittest.mock import MagicMock
    import requests
    from backend.config import Config

    monkeypatch.setattr(Config, "GROQ_API_KEY", "gsk_test_fake_key_123")
    monkeypatch.setattr(Config, "GROQ_MODEL", "llama-3.3-70b-versatile")

    # Step 1: Groq returns tool call to list tasks
    tool_call_resp = MagicMock()
    tool_call_resp.status_code = 200
    tool_call_resp.json.return_value = {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [
                        {
                            "id": "call_12345",
                            "type": "function",
                            "function": {
                                "name": "list_tasks",
                                "arguments": '{"status": "pending"}'
                            }
                        }
                    ]
                }
            }
        ]
    }

    # Step 2: Groq receives tool results and produces final answer
    final_resp = MagicMock()
    final_resp.status_code = 200
    final_resp.json.return_value = {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": "You have 2 pending tasks on your board."
                }
            }
        ]
    }

    call_count = {"count": 0}
    def mock_post_dispatcher(url, **kwargs):
        call_count["count"] += 1
        if call_count["count"] == 1:
            return tool_call_resp
        return final_resp

    with monkeypatch.context() as m:
        m.setattr(requests, "post", mock_post_dispatcher)
        res = client.post("/api/chat", json={"message": "What pending tasks do I have?"})
        assert res.status_code == 200
        data = res.get_json()
        assert data["success"] is True
        assert data["data"]["source"] == "groq"
        assert "You have 2 pending tasks" in data["data"]["response"]
        assert call_count["count"] == 2

def test_groq_api_failure_falls_back_gracefully(client, monkeypatch):
    from unittest.mock import MagicMock
    import requests
    from backend.config import Config

    monkeypatch.setattr(Config, "GROQ_API_KEY", "gsk_invalid_key_error")
    mock_err_resp = MagicMock()
    mock_err_resp.status_code = 401
    mock_err_resp.text = '{"error": {"message": "Invalid API Key"}}'

    with monkeypatch.context() as m:
        m.setattr(requests, "post", lambda url, **kwargs: mock_err_resp)
        # Should smoothly fall back to local FAQ or error engine without 500 error
        res = client.post("/api/chat", json={"message": "What is TaskMate?"})
        assert res.status_code == 200
        data = res.get_json()
        assert data["success"] is True
        assert data["data"]["source"] == "local_faq"
        assert "TaskMate" in data["data"]["response"]
