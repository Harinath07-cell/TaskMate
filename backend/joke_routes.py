from flask import Blueprint, jsonify
from backend.joke_service import fetch_programming_joke

joke_bp = Blueprint("joke", __name__, url_prefix="/api/joke")

@joke_bp.route("", methods=["GET"])
def get_joke():
    """Retrieve a programming joke from external API with timeout and offline fallback."""
    joke = fetch_programming_joke()
    return jsonify({
        "success": True,
        "data": joke
    }), 200
