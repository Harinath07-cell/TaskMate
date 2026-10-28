import uuid
from flask import Blueprint, request, jsonify
from backend.ai_service import AIService, check_rate_limit
from backend.mongo_client import mongo_service
from backend.config import Config

chat_bp = Blueprint("chat", __name__, url_prefix="/api/chat")

@chat_bp.route("", methods=["POST"])
def send_chat_message():
    """Handles chatbot queries, grounding, AI responses, and MongoDB logging."""
    # Rate limit check (HTTP 429)
    client_ip = request.remote_addr or "127.0.0.1"
    if not check_rate_limit(client_ip, max_requests=Config.CHAT_RATE_LIMIT, window_seconds=60):
        return jsonify({
            "success": False,
            "error": {
                "code": "429",
                "message": "Too many requests. Please wait a moment before sending another message."
            }
        }), 429

    data = request.get_json(silent=True)
    if not data:
        return jsonify({
            "success": False,
            "error": {"code": "400", "message": "Invalid JSON body provided."}
        }), 400

    message = str(data.get("message", "")).strip()
    if not message:
        return jsonify({
            "success": False,
            "error": {"code": "400", "message": "Message text cannot be empty."}
        }), 400

    if len(message) > 500:
        return jsonify({
            "success": False,
            "error": {"code": "400", "message": "Message exceeds maximum allowed length of 500 characters."}
        }), 400

    conversation_id = data.get("conversation_id") or str(uuid.uuid4())
    user_msg_id = str(uuid.uuid4())
    assistant_msg_id = str(uuid.uuid4())

    # Log user message to MongoDB
    mongo_service.log_chat_message(
        conversation_id=conversation_id,
        message_id=user_msg_id,
        role="user",
        content=message
    )

    # Process message through grounded AI service
    ai_result = AIService.process_message(message, conversation_id=conversation_id)

    # Log assistant response to MongoDB
    mongo_service.log_chat_message(
        conversation_id=conversation_id,
        message_id=assistant_msg_id,
        role="assistant",
        content=ai_result["response"]
    )

    return jsonify({
        "success": True,
        "data": {
            "conversation_id": conversation_id,
            "message_id": assistant_msg_id,
            "response": ai_result["response"],
            "suggest_ticket": ai_result.get("suggest_ticket", False),
            "source": ai_result.get("source", "unknown")
        }
    }), 200

@chat_bp.route("/feedback", methods=["POST"])
def submit_feedback():
    """Stores chatbot response feedback in MongoDB."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({
            "success": False,
            "error": {"code": "400", "message": "Invalid JSON body."}
        }), 400

    conversation_id = str(data.get("conversation_id", "")).strip()
    message_id = str(data.get("message_id", "")).strip()
    rating = str(data.get("rating", "")).strip().lower()
    comment = data.get("comment")

    if not conversation_id or not message_id:
        return jsonify({
            "success": False,
            "error": {"code": "400", "message": "conversation_id and message_id are required."}
        }), 400

    if rating not in ("helpful", "not_helpful"):
        return jsonify({
            "success": False,
            "error": {"code": "400", "message": "Rating must be either 'helpful' or 'not_helpful'."}
        }), 400

    # Store in MongoDB
    logged = mongo_service.log_feedback(
        conversation_id=conversation_id,
        message_id=message_id,
        rating=rating,
        comment=str(comment).strip() if comment else None
    )

    return jsonify({
        "success": True,
        "message": "Thank you for your feedback!",
        "logged_to_mongodb": logged
    }), 200
