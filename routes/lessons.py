import json
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from database.database import get_db_connection
from config import Config

lessons_bp = Blueprint("lessons", __name__, url_prefix="/lessons")

def load_lessons_data():
    lessons_file = Config.DATA_DIR / "lessons.json"
    if lessons_file.exists():
        with open(lessons_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

@lessons_bp.route("/")
def list_lessons():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM lessons ORDER BY day_number ASC")
    db_lessons = {row["day_number"]: dict(row) for row in c.fetchall()}
    conn.close()

    full_lessons = load_lessons_data()
    # Merge completion status
    for lesson in full_lessons:
        day = lesson["day_number"]
        lesson["completed"] = db_lessons.get(day, {}).get("completed", 0)

    completed_count = sum(1 for l in full_lessons if l.get("completed") == 1)
    progress_pct = round((completed_count / len(full_lessons)) * 100, 1) if full_lessons else 0

    return render_template(
        "lessons.html",
        lessons=full_lessons,
        completed_count=completed_count,
        total_count=len(full_lessons),
        progress_pct=progress_pct
    )

@lessons_bp.route("/<int:day>")
def lesson_detail(day):
    full_lessons = load_lessons_data()
    lesson = next((l for l in full_lessons if l["day_number"] == day), None)
    if not lesson:
        return redirect(url_for("lessons.list_lessons"))

    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT completed FROM lessons WHERE day_number = ?", (day,))
    row = c.fetchone()
    completed = row["completed"] if row else 0
    conn.close()

    lesson["completed"] = completed
    prev_day = day - 1 if day > 1 else None
    next_day = day + 1 if day < len(full_lessons) else None

    return render_template(
        "lesson_detail.html",
        lesson=lesson,
        prev_day=prev_day,
        next_day=next_day
    )

@lessons_bp.route("/<int:day>/toggle", methods=["POST"])
@lessons_bp.route("/toggle-complete/<int:day>", methods=["POST"])
def toggle_completion(day):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT completed FROM lessons WHERE day_number = ?", (day,))
    row = c.fetchone()
    new_status = 1 if (row and row["completed"] == 0) else 0
    
    c.execute("""
        UPDATE lessons 
        SET completed = ?, completed_at = CURRENT_TIMESTAMP 
        WHERE day_number = ?
    """, (new_status, day))
    conn.commit()
    conn.close()
    
    return jsonify({"success": True, "day": day, "completed": bool(new_status)})
