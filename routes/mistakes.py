import json
from flask import Blueprint, render_template, request, jsonify
from database.database import get_db_connection
from config import Config

mistakes_bp = Blueprint("mistakes", __name__, url_prefix="/mistakes")

@mistakes_bp.route("/")
def index():
    category = request.args.get("category", "").strip()
    status = request.args.get("status", "")  # '0' = pending, '1' = reviewed
    source = request.args.get("source", "").strip() # 'grammar_checker', 'conversation', 'quiz'
    search = request.args.get("search", "").strip()

    conn = get_db_connection()
    c = conn.cursor()

    # Get distinct categories
    c.execute("SELECT DISTINCT mistake_category FROM mistake_log ORDER BY mistake_category ASC")
    categories = [row["mistake_category"] for row in c.fetchall()]

    query = "SELECT * FROM mistake_log WHERE 1=1"
    params = []

    if category:
        query += " AND mistake_category = ?"
        params.append(category)

    if source:
        query += " AND source = ?"
        params.append(source)

    if status == "0":
        query += " AND reviewed = 0"
    elif status == "1":
        query += " AND reviewed = 1"

    if search:
        query += " AND (original_sentence LIKE ? OR corrected_sentence LIKE ? OR explanation_en LIKE ? OR explanation_ta LIKE ?)"
        pattern = f"%{search}%"
        params.extend([pattern, pattern, pattern, pattern])

    query += " ORDER BY id DESC"
    c.execute(query, params)
    mistakes = [dict(row) for row in c.fetchall()]

    # Stats
    c.execute("SELECT COUNT(*) FROM mistake_log")
    total_count = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM mistake_log WHERE reviewed = 1")
    reviewed_count = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM mistake_log WHERE reviewed = 0")
    pending_count = c.fetchone()[0]

    conn.close()

    return render_template(
        "mistake_log.html",
        mistakes=mistakes,
        categories=categories,
        current_category=category,
        current_status=status,
        current_source=source,
        search_query=search,
        total_count=total_count,
        reviewed_count=reviewed_count,
        pending_count=pending_count
    )

@mistakes_bp.route("/toggle-review", methods=["POST"])
def toggle_review():
    data = request.get_json() or {}
    mistake_id = data.get("id")
    if not mistake_id:
        return jsonify({"error": "Missing mistake ID"}), 400

    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT reviewed FROM mistake_log WHERE id = ?", (mistake_id,))
    row = c.fetchone()
    if not row:
        conn.close()
        return jsonify({"error": "Not found"}), 404

    new_status = 0 if row["reviewed"] == 1 else 1
    c.execute("UPDATE mistake_log SET reviewed = ? WHERE id = ?", (new_status, mistake_id))
    conn.commit()
    conn.close()

    return jsonify({"success": True, "id": mistake_id, "reviewed": bool(new_status)})

@mistakes_bp.route("/before-after")
def before_after():
    assessment_file = Config.DATA_DIR / "assessment_data.json"
    data = {}
    if assessment_file.exists():
        with open(assessment_file, "r", encoding="utf-8") as f:
            data = json.load(f)

    return render_template(
        "before_after.html",
        baseline=data.get("baseline_day_1", {}),
        final=data.get("final_day_14", {}),
        improvements=data.get("metric_improvements", [])
    )
