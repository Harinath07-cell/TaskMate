from flask import Blueprint, jsonify
from backend.error_definitions import get_all_errors, get_error

error_bp = Blueprint("errors", __name__, url_prefix="/api/errors")

@error_bp.route("", methods=["GET"])
def list_errors():
    """Return all supported error code definitions including DEV001."""
    errors = get_all_errors()
    return jsonify({
        "success": True,
        "count": len(errors),
        "data": errors
    }), 200

@error_bp.route("/<code>", methods=["GET"])
def get_error_detail(code):
    """Return definition for a specific error code."""
    error_def = get_error(code)
    if not error_def:
        return jsonify({
            "success": False,
            "error": {"code": "404", "message": f"Error code '{code}' is not documented in TaskMate."}
        }), 404
    return jsonify({
        "success": True,
        "data": error_def
    }), 200

# Simulated Error Test Endpoints (for demonstration, automated testing, and verification)
@error_bp.route("/test/400", methods=["GET"])
def test_400():
    return jsonify({
        "success": False,
        "error": {
            "code": "400",
            "name": "Bad Request",
            "message": "Demonstration 400 error: Missing mandatory parameter."
        }
    }), 400

@error_bp.route("/test/401", methods=["GET"])
def test_401():
    return jsonify({
        "success": False,
        "error": {
            "code": "401",
            "name": "Unauthorized",
            "message": "Demonstration 401 error: Authentication token missing or invalid."
        }
    }), 401

@error_bp.route("/test/403", methods=["GET"])
def test_403():
    return jsonify({
        "success": False,
        "error": {
            "code": "403",
            "name": "Forbidden",
            "message": "Demonstration 403 error: Access to this administrative resource is forbidden."
        }
    }), 403

@error_bp.route("/test/404", methods=["GET"])
def test_404():
    return jsonify({
        "success": False,
        "error": {
            "code": "404",
            "name": "Not Found",
            "message": "Demonstration 404 error: The requested demonstration resource does not exist."
        }
    }), 404

@error_bp.route("/test/429", methods=["GET"])
def test_429():
    return jsonify({
        "success": False,
        "error": {
            "code": "429",
            "name": "Too Many Requests",
            "message": "Demonstration 429 error: Rate limit exceeded. Please wait 30 seconds."
        }
    }), 429

@error_bp.route("/test/500", methods=["GET"])
def test_500():
    return jsonify({
        "success": False,
        "error": {
            "code": "500",
            "name": "Internal Server Error",
            "message": "Demonstration 500 error: An unexpected server-side error was simulated."
        }
    }), 500

@error_bp.route("/test/503", methods=["GET"])
def test_503():
    return jsonify({
        "success": False,
        "error": {
            "code": "503",
            "name": "Service Unavailable",
            "message": "Demonstration 503 error: Service is temporarily undergoing scheduled maintenance."
        }
    }), 503

@error_bp.route("/test/dev001", methods=["GET"])
def test_dev001():
    return jsonify({
        "success": False,
        "error": {
            "code": "DEV001",
            "name": "TaskMate Application Error",
            "message": "Demonstration DEV001 error: Internal task-processing logic exception occurred."
        }
    }), 422
