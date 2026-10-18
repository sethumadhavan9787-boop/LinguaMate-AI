from flask import Blueprint, render_template, request
from database.database import get_db_connection

poster_bp = Blueprint("poster", __name__, url_prefix="/poster")

TOPIC_ICONS = {
    "Greetings": "bi-hand-thumbs-up-fill",
    "Family": "bi-people-fill",
    "Food": "bi-cup-hot-fill",
    "Education": "bi-mortarboard-fill",
    "Travel": "bi-compass-fill",
    "Daily Activities": "bi-clock-history",
    "Emotions": "bi-emoji-smile-fill",
    "Workplace": "bi-briefcase-fill"
}

@poster_bp.route("/")
def index():
    topic = request.args.get("topic", "Greetings")
    
    conn = get_db_connection()
    c = conn.cursor()
    
    # Get available categories
    c.execute("SELECT DISTINCT category FROM vocabulary ORDER BY category ASC")
    categories = [row["category"] for row in c.fetchall()]
    
    # Get 10 words for the chosen topic
    c.execute("""
        SELECT * FROM vocabulary 
        WHERE category = ? 
        ORDER BY id ASC LIMIT 10
    """, (topic,))
    words = [dict(row) for row in c.fetchall()]
    
    # Fallback if less than 10
    if len(words) < 10:
        c.execute("SELECT * FROM vocabulary ORDER BY id ASC LIMIT 10")
        words = [dict(row) for row in c.fetchall()]

    conn.close()

    topic_icon = TOPIC_ICONS.get(topic, "bi-book-half")

    return render_template(
        "poster.html",
        categories=categories,
        current_topic=topic,
        words=words,
        topic_icon=topic_icon
    )
