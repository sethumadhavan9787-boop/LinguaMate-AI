from flask import Blueprint, render_template
from database.database import get_db_connection, get_dashboard_metrics

reports_bp = Blueprint("reports", __name__, url_prefix="/reports")

@reports_bp.route("/")
def index():
    metrics = get_dashboard_metrics()
    
    conn = get_db_connection()
    c = conn.cursor()
    
    # 1. Lesson Completion Progress
    c.execute("SELECT day_number, title, completed FROM lessons ORDER BY day_number ASC")
    lessons_data = [dict(row) for row in c.fetchall()]
    
    # 2. Quiz performance
    c.execute("SELECT id, category, score, total_questions, percentage, attempted_at FROM quiz_attempts ORDER BY id ASC")
    quiz_attempts = [dict(row) for row in c.fetchall()]
    
    # 3. Mistake category distribution
    c.execute("""
        SELECT mistake_category, COUNT(*) as count 
        FROM mistake_log 
        GROUP BY mistake_category 
        ORDER BY count DESC LIMIT 8
    """)
    mistake_distribution = [dict(row) for row in c.fetchall()]

    # 4. Verified AI Comparison data
    c.execute("SELECT * FROM ai_comparisons ORDER BY sentence_id ASC")
    comparison_cases = [dict(row) for row in c.fetchall()]
    
    conn.close()

    return render_template(
        "reports.html",
        metrics=metrics,
        lessons=lessons_data,
        quiz_attempts=quiz_attempts,
        mistake_distribution=mistake_distribution,
        comparison_cases=comparison_cases
    )
