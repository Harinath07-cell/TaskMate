import re
import uuid
from datetime import datetime, timezone
from flask import Blueprint, request, jsonify
from backend.database import db

ticket_bp = Blueprint("tickets", __name__, url_prefix="/api/tickets")

EMAIL_REGEX = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

def generate_ticket_code():
    """Generates a collision-resistant human-readable ticket code e.g. TKT-2026-ABCD."""
    year = datetime.now().year
    suffix = uuid.uuid4().hex[:4].upper()
    return f"TKT-{year}-{suffix}"

@ticket_bp.route("", methods=["POST"])
def create_ticket():
    """Create a new support ticket."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({
            "success": False,
            "error": {"code": "400", "message": "Invalid JSON body provided."}
        }), 400

    title = str(data.get("title", "")).strip()
    desc = str(data.get("description", "")).strip()
    email = data.get("email")

    errors = []
    if not title:
        errors.append("Ticket title is required.")
    elif len(title) > 255:
        errors.append("Ticket title cannot exceed 255 characters.")

    if not desc:
        errors.append("Ticket description is required.")

    sanitized_email = None
    if email:
        email_str = str(email).strip()
        if email_str:
            if not re.match(EMAIL_REGEX, email_str):
                errors.append("Invalid email address format.")
            else:
                sanitized_email = email_str

    if errors:
        return jsonify({
            "success": False,
            "error": {"code": "400", "message": "; ".join(errors)}
        }), 400

    # Ensure unique ticket code
    ticket_code = generate_ticket_code()
    max_attempts = 5
    inserted = False
    for _ in range(max_attempts):
        try:
            sql = """
                INSERT INTO support_tickets (ticket_code, title, description, email, status)
                VALUES (%s, %s, %s, %s, 'OPEN')
            """
            db.execute_query(sql, (ticket_code, title, desc, sanitized_email))
            inserted = True
            break
        except Exception:
            ticket_code = generate_ticket_code()

    if not inserted:
        return jsonify({
            "success": False,
            "error": {"code": "DEV001", "message": "Failed to create support ticket. Please retry."}
        }), 500

    return jsonify({
        "success": True,
        "message": f"Your support ticket has been created successfully. Ticket ID: {ticket_code}.",
        "data": {
            "ticket_code": ticket_code,
            "title": title,
            "status": "OPEN",
            "email_notified": bool(sanitized_email)
        }
    }), 201

@ticket_bp.route("/<ticket_code>", methods=["GET"])
def get_ticket_status(ticket_code):
    """Retrieve public ticket status safely."""
    code_clean = str(ticket_code).strip().upper()
    try:
        ticket = db.fetch_one(
            "SELECT ticket_code, title, status, created_at, updated_at FROM support_tickets WHERE UPPER(ticket_code) = %s",
            (code_clean,)
        )
        if not ticket:
            return jsonify({
                "success": False,
                "error": {"code": "404", "message": f"Ticket '{ticket_code}' not found."}
            }), 404

        return jsonify({
            "success": True,
            "data": ticket
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": {"code": "500", "message": "Failed to fetch ticket status."}
        }), 500
