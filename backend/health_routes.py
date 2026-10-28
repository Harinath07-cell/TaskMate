from flask import Blueprint, jsonify
from backend.database import db
from backend.mongo_client import mongo_service
from backend.config import Config

health_bp = Blueprint("health", __name__, url_prefix="/health")

@health_bp.route("", methods=["GET"])
def health_check():
    """
    Application health check endpoint.
    Reports operational status of the Flask application, relational database (MySQL/SQLite fallback),
    MongoDB logging service, and AI assistant provider.
    """
    db_ok, db_driver = db.check_connection()
    mongo_ok, _ = mongo_service.check_connection()

    if Config.GROQ_API_KEY:
        ai_provider = "groq"
        ai_model = Config.GROQ_MODEL
        ai_status = "configured"
    elif Config.GEMINI_API_KEY:
        ai_provider = "google-gemini"
        ai_model = Config.AI_MODEL
        ai_status = "configured"
    else:
        ai_provider = "grounded-local-fallback"
        ai_model = "embedded-rule-grounding"
        ai_status = "fallback_mode"

    overall_healthy = db_ok  # Relational database is the critical dependency

    status_code = 200 if overall_healthy else 503

    return jsonify({
        "status": "healthy" if overall_healthy else "degraded",
        "service": "TaskMate API",
        "version": "1.0.0",
        "dependencies": {
            "database": {
                "status": "connected" if db_ok else "unreachable",
                "engine": db_driver if db_ok else "none",
                "critical": True
            },
            "mongodb": {
                "status": "connected" if mongo_ok else "unavailable_offline_logging",
                "critical": False
            },
            "ai_assistant": {
                "provider": ai_provider,
                "status": ai_status,
                "model": ai_model,
                "critical": False
            }
        }
    }), status_code
