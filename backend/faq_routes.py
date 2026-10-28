from flask import Blueprint, request, jsonify
from backend.database import db

faq_bp = Blueprint("faqs", __name__, url_prefix="/api/faqs")

@faq_bp.route("", methods=["GET"])
def get_faqs():
    """Retrieve all FAQs stored in the database."""
    try:
        faqs = db.fetch_all("SELECT * FROM faqs ORDER BY id ASC")
        return jsonify({
            "success": True,
            "count": len(faqs),
            "data": faqs
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": {"code": "500", "message": "Failed to retrieve FAQs."}
        }), 500

@faq_bp.route("/search", methods=["GET"])
def search_faqs():
    """Search FAQs by question or answer keyword."""
    query = request.args.get("q", "").strip()
    if not query:
        # Return all faqs if query is empty
        try:
            faqs = db.fetch_all("SELECT * FROM faqs ORDER BY id ASC")
            return jsonify({
                "success": True,
                "count": len(faqs),
                "data": faqs,
                "query": ""
            }), 200
        except Exception as e:
            return jsonify({
                "success": False,
                "error": {"code": "500", "message": "Failed to search FAQs."}
            }), 500

    try:
        sql = "SELECT * FROM faqs WHERE LOWER(question) LIKE %s OR LOWER(answer) LIKE %s ORDER BY id ASC"
        term = f"%{query.lower()}%"
        matches = db.fetch_all(sql, (term, term))
        return jsonify({
            "success": True,
            "count": len(matches),
            "query": query,
            "data": matches
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": {"code": "500", "message": "Error searching FAQs."}
        }), 500

@faq_bp.route("/<int:faq_id>", methods=["GET"])
def get_faq(faq_id):
    """Retrieve a single FAQ by its ID."""
    try:
        faq = db.fetch_one("SELECT * FROM faqs WHERE id = %s", (faq_id,))
        if not faq:
            return jsonify({
                "success": False,
                "error": {"code": "404", "message": f"FAQ with ID {faq_id} not found."}
            }), 404
        return jsonify({"success": True, "data": faq}), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": {"code": "500", "message": "Internal error fetching FAQ."}
        }), 500
