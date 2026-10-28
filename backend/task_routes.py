import re
from datetime import datetime
from flask import Blueprint, request, jsonify
from backend.database import db

task_bp = Blueprint("tasks", __name__, url_prefix="/api/tasks")

VALID_PRIORITIES = {"Low", "Medium", "High"}

def validate_task_data(data, is_update=False):
    """Validates task fields and returns (errors_list, sanitized_data)."""
    errors = []
    sanitized = {}

    title = data.get("title")
    if title is not None:
        title = str(title).strip()
        if not title:
            errors.append("Task title cannot be empty.")
        elif len(title) > 255:
            errors.append("Task title must be 255 characters or fewer.")
        sanitized["title"] = title
    elif not is_update:
        errors.append("Task title is required.")

    desc = data.get("description")
    if desc is not None:
        sanitized["description"] = str(desc).strip() if str(desc).strip() else None
    elif not is_update:
        sanitized["description"] = None

    priority = data.get("priority")
    if priority is not None:
        priority_clean = str(priority).strip().capitalize()
        if priority_clean not in VALID_PRIORITIES:
            errors.append(f"Priority must be one of: {', '.join(VALID_PRIORITIES)}.")
        else:
            sanitized["priority"] = priority_clean
    elif not is_update:
        sanitized["priority"] = "Medium"

    due_date = data.get("due_date")
    if due_date:
        due_date_str = str(due_date).strip()
        if due_date_str:
            try:
                datetime.strptime(due_date_str, "%Y-%m-%d")
                sanitized["due_date"] = due_date_str
            except ValueError:
                errors.append("Due date must be in YYYY-MM-DD format.")
        else:
            sanitized["due_date"] = None
    elif due_date == "" or due_date is None:
        sanitized["due_date"] = None

    return errors, sanitized

@task_bp.route("", methods=["GET"])
def get_tasks():
    """Retrieve all tasks with optional status filter (?status=pending|completed|all)."""
    status_filter = request.args.get("status", "all").lower()
    try:
        if status_filter == "pending":
            sql = "SELECT * FROM tasks WHERE is_completed = 0 ORDER BY priority = 'High' DESC, due_date ASC, created_at DESC"
            tasks = db.fetch_all(sql)
        elif status_filter == "completed":
            sql = "SELECT * FROM tasks WHERE is_completed = 1 ORDER BY updated_at DESC"
            tasks = db.fetch_all(sql)
        else:
            sql = "SELECT * FROM tasks ORDER BY is_completed ASC, priority = 'High' DESC, created_at DESC"
            tasks = db.fetch_all(sql)

        # Normalize is_completed to boolean
        for t in tasks:
            t["is_completed"] = bool(t["is_completed"])

        return jsonify({
            "success": True,
            "count": len(tasks),
            "data": tasks
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": {"code": "DEV001", "message": "Failed to retrieve tasks from database."}
        }), 500

@task_bp.route("/<int:task_id>", methods=["GET"])
def get_task(task_id):
    """Retrieve a single task by ID."""
    try:
        task = db.fetch_one("SELECT * FROM tasks WHERE id = %s", (task_id,))
        if not task:
            return jsonify({
                "success": False,
                "error": {"code": "404", "message": f"Task with ID {task_id} not found."}
            }), 404
        task["is_completed"] = bool(task["is_completed"])
        return jsonify({"success": True, "data": task}), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": {"code": "500", "message": "Internal error fetching task."}
        }), 500

@task_bp.route("", methods=["POST"])
def create_task():
    """Create a new task."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({
            "success": False,
            "error": {"code": "400", "message": "Invalid JSON body provided."}
        }), 400

    errors, sanitized = validate_task_data(data)
    if errors:
        return jsonify({
            "success": False,
            "error": {"code": "400", "message": "; ".join(errors)}
        }), 400

    try:
        sql = """
            INSERT INTO tasks (title, description, priority, due_date, is_completed)
            VALUES (%s, %s, %s, %s, 0)
        """
        last_id, _ = db.execute_query(
            sql,
            (sanitized["title"], sanitized["description"], sanitized["priority"], sanitized["due_date"])
        )
        created_task = db.fetch_one("SELECT * FROM tasks WHERE id = %s", (last_id,))
        if created_task:
            created_task["is_completed"] = bool(created_task["is_completed"])
        return jsonify({"success": True, "data": created_task}), 201
    except Exception as e:
        return jsonify({
            "success": False,
            "error": {"code": "DEV001", "message": "Failed to create task."}
        }), 500

@task_bp.route("/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    """Update an existing task."""
    existing = db.fetch_one("SELECT * FROM tasks WHERE id = %s", (task_id,))
    if not existing:
        return jsonify({
            "success": False,
            "error": {"code": "404", "message": f"Task with ID {task_id} not found."}
        }), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({
            "success": False,
            "error": {"code": "400", "message": "Invalid JSON payload."}
        }), 400

    errors, sanitized = validate_task_data(data, is_update=True)
    if errors:
        return jsonify({
            "success": False,
            "error": {"code": "400", "message": "; ".join(errors)}
        }), 400

    # Build update clause
    fields = []
    params = []
    for k, v in sanitized.items():
        fields.append(f"{k} = %s")
        params.append(v)

    if not fields:
        return jsonify({"success": True, "data": existing}), 200

    params.append(task_id)
    sql = f"UPDATE tasks SET {', '.join(fields)} WHERE id = %s"
    try:
        db.execute_query(sql, tuple(params))
        updated_task = db.fetch_one("SELECT * FROM tasks WHERE id = %s", (task_id,))
        updated_task["is_completed"] = bool(updated_task["is_completed"])
        return jsonify({"success": True, "data": updated_task}), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": {"code": "DEV001", "message": "Failed to update task."}
        }), 500

@task_bp.route("/<int:task_id>/complete", methods=["PATCH"])
def complete_task(task_id):
    """Mark a task as completed."""
    existing = db.fetch_one("SELECT * FROM tasks WHERE id = %s", (task_id,))
    if not existing:
        return jsonify({
            "success": False,
            "error": {"code": "404", "message": f"Task with ID {task_id} not found."}
        }), 404

    try:
        db.execute_query("UPDATE tasks SET is_completed = 1 WHERE id = %s", (task_id,))
        updated = db.fetch_one("SELECT * FROM tasks WHERE id = %s", (task_id,))
        updated["is_completed"] = bool(updated["is_completed"])
        return jsonify({"success": True, "data": updated}), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": {"code": "DEV001", "message": "Could not complete task."}
        }), 500

@task_bp.route("/<int:task_id>/reopen", methods=["PATCH"])
def reopen_task(task_id):
    """Reopen a completed task."""
    existing = db.fetch_one("SELECT * FROM tasks WHERE id = %s", (task_id,))
    if not existing:
        return jsonify({
            "success": False,
            "error": {"code": "404", "message": f"Task with ID {task_id} not found."}
        }), 404

    try:
        db.execute_query("UPDATE tasks SET is_completed = 0 WHERE id = %s", (task_id,))
        updated = db.fetch_one("SELECT * FROM tasks WHERE id = %s", (task_id,))
        updated["is_completed"] = bool(updated["is_completed"])
        return jsonify({"success": True, "data": updated}), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": {"code": "DEV001", "message": "Could not reopen task."}
        }), 500

@task_bp.route("/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    """Delete a task."""
    existing = db.fetch_one("SELECT * FROM tasks WHERE id = %s", (task_id,))
    if not existing:
        return jsonify({
            "success": False,
            "error": {"code": "404", "message": f"Task with ID {task_id} not found."}
        }), 404

    try:
        db.execute_query("DELETE FROM tasks WHERE id = %s", (task_id,))
        return jsonify({
            "success": True,
            "message": f"Task {task_id} deleted successfully."
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": {"code": "DEV001", "message": "Could not delete task."}
        }), 500
