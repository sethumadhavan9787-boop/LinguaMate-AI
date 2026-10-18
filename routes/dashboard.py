from flask import Blueprint, render_template, jsonify
from database.database import get_dashboard_metrics, get_db_connection

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
@dashboard_bp.route("/dashboard")
def index():
    metrics = get_dashboard_metrics()
    
    # Fetch quiz score history for chart (only completed quizzes)
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""
        SELECT percentage, category, attempted_at 
        FROM quiz_attempts 
        WHERE is_completed = 1 OR answered_questions >= total_questions 
        ORDER BY id ASC 
        LIMIT 10
    """)
    quiz_history = [dict(row) for row in c.fetchall()]
    
    # Fetch recent mistakes
    c.execute("SELECT * FROM mistake_log ORDER BY id DESC LIMIT 5")
    recent_mistakes = [dict(row) for row in c.fetchall()]
    
    # Fetch today's recommended lesson
    c.execute("SELECT * FROM lessons WHERE completed = 0 ORDER BY day_number ASC LIMIT 1")
    next_lesson_row = c.fetchone()
    next_lesson = dict(next_lesson_row) if next_lesson_row else {"day_number": 14, "title": "Day 14: Final Capstone Assessment"}

    conn.close()
    
    return render_template(
        "dashboard.html",
        metrics=metrics,
        quiz_history=quiz_history,
        recent_mistakes=recent_mistakes,
        next_lesson=next_lesson
    )

@dashboard_bp.route("/api/chart-data")
def chart_data():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""
        SELECT percentage, category, attempted_at 
        FROM quiz_attempts 
        WHERE is_completed = 1 OR answered_questions >= total_questions 
        ORDER BY id ASC 
        LIMIT 10
    """)
    quiz_history = [dict(row) for row in c.fetchall()]
    conn.close()
    
    return jsonify({
        "success": True,
        "completed_count": len(quiz_history),
        "quiz_history": quiz_history
    })

