from flask import Blueprint, render_template, request, jsonify
from database.database import get_db_connection

responsible_ai_bp = Blueprint("responsible_ai", __name__, url_prefix="/responsible-ai")

@responsible_ai_bp.route("/")
def index():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM questionable_reports ORDER BY id DESC LIMIT 10")
    recent_reports = [dict(row) for row in c.fetchall()]
    conn.close()

    return render_template(
        "responsible_ai.html",
        recent_reports=recent_reports
    )

@responsible_ai_bp.route("/report", methods=["POST"])
def submit_report():
    data = request.get_json() or {}
    module = data.get("module", "General").strip()
    input_text = data.get("input_text", "").strip()
    ai_response = data.get("ai_response", "").strip()
    issue_category = data.get("issue_category", "Hallucination").strip()
    user_notes = data.get("user_notes", "").strip()

    if not input_text or not issue_category:
        return jsonify({"error": "Missing required fields"}), 400

    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""
        INSERT INTO questionable_reports (module, input_text, ai_response, issue_category, user_notes)
        VALUES (?, ?, ?, ?, ?)
    """, (module, input_text, ai_response, issue_category, user_notes))
    conn.commit()
    conn.close()

    return jsonify({
        "success": True, 
        "message": "Report logged successfully. Thank you for contributing to responsible AI evaluation!"
    })
