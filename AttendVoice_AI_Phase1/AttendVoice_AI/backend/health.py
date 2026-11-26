from flask import Blueprint, jsonify, current_app
from sqlalchemy import text
from database.db import db

health_bp = Blueprint("health", __name__, url_prefix="/api")

@health_bp.get("/health")
def health():
    try:
        db.session.execute(text("SELECT 1"))
        database_status = "connected"
    except Exception:
        db.session.rollback()
        database_status = "disconnected"
    status_code = 200 if database_status == "connected" else 503
    return jsonify({
        "application": "AttendVoice AI",
        "status": "healthy" if status_code == 200 else "degraded",
        "database": database_status,
        "college": current_app.config["COLLEGE_NAME"]
    }), status_code
