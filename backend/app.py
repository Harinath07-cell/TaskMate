import os
from pathlib import Path
from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
from backend.config import Config
from backend.logging_config import setup_logging
from backend.task_routes import task_bp
from backend.faq_routes import faq_bp
from backend.ticket_routes import ticket_bp
from backend.error_routes import error_bp
from backend.chat_routes import chat_bp
from backend.joke_routes import joke_bp
from backend.health_routes import health_bp

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

def create_app():
    app = Flask(__name__, static_folder=str(FRONTEND_DIR))
    app.config.from_object(Config)

    # Setup CORS for API endpoints
    CORS(app, resources={r"/api/*": {"origins": Config.FRONTEND_ORIGIN}, r"/health": {"origins": "*"}})

    # Setup Request Logging
    setup_logging(app)

    # Register Blueprints
    app.register_blueprint(task_bp)
    app.register_blueprint(faq_bp)
    app.register_blueprint(ticket_bp)
    app.register_blueprint(error_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(joke_bp)
    app.register_blueprint(health_bp)

    # Frontend Page Routes
    @app.route("/")
    def serve_home():
        return send_from_directory(FRONTEND_DIR, "index.html")

    @app.route("/faq")
    def serve_faq():
        return send_from_directory(FRONTEND_DIR, "faq.html")

    @app.route("/errors")
    def serve_errors():
        return send_from_directory(FRONTEND_DIR, "errors.html")

    @app.route("/about")
    def serve_about():
        return send_from_directory(FRONTEND_DIR, "about.html")

    # Static Assets Handlers
    @app.route("/css/<path:filename>")
    def serve_css(filename):
        return send_from_directory(FRONTEND_DIR / "css", filename)

    @app.route("/js/<path:filename>")
    def serve_js(filename):
        return send_from_directory(FRONTEND_DIR / "js", filename)

    @app.route("/assets/<path:filename>")
    def serve_assets(filename):
        return send_from_directory(FRONTEND_DIR / "assets", filename)

    # Custom Error Handlers
    @app.errorhandler(404)
    def handle_404(e):
        if request.path.startswith("/api/") or request.accept_mimetypes.best == "application/json":
            return jsonify({
                "success": False,
                "error": {
                    "code": "404",
                    "message": f"Endpoint '{request.path}' was not found on this server."
                }
            }), 404
        return send_from_directory(FRONTEND_DIR, "404.html"), 404

    @app.errorhandler(500)
    def handle_500(e):
        if request.path.startswith("/api/") or request.accept_mimetypes.best == "application/json":
            return jsonify({
                "success": False,
                "error": {
                    "code": "500",
                    "message": "An unexpected internal server error occurred."
                }
            }), 500
        return send_from_directory(FRONTEND_DIR, "500.html"), 500

    @app.errorhandler(429)
    def handle_429(e):
        return jsonify({
            "success": False,
            "error": {
                "code": "429",
                "message": "Too many requests. Please slow down."
            }
        }), 429

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Config.PORT, debug=Config.DEBUG)
