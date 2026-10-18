from flask import Blueprint, render_template, request, jsonify
from database.database import get_db_connection

vocabulary_bp = Blueprint("vocabulary", __name__, url_prefix="/vocabulary")

@vocabulary_bp.route("/")
def index():
    category = request.args.get("category", "")
    search = request.args.get("search", "").strip()
    favorites_only = request.args.get("favorites", "0") == "1"

    conn = get_db_connection()
    c = conn.cursor()

    # Get all distinct categories
    c.execute("SELECT DISTINCT category FROM vocabulary ORDER BY category ASC")
    categories = [row["category"] for row in c.fetchall()]

    query = "SELECT * FROM vocabulary WHERE 1=1"
    params = []

    if category:
        query += " AND category = ?"
        params.append(category)

    if search:
        query += " AND (word LIKE ? OR tamil_meaning LIKE ? OR example_sentence LIKE ?)"
        pattern = f"%{search}%"
        params.extend([pattern, pattern, pattern])

    if favorites_only:
        query += " AND is_favorite = 1"

    query += " ORDER BY word ASC"
    c.execute(query, params)
    words = [dict(row) for row in c.fetchall()]

    c.execute("SELECT COUNT(*) FROM vocabulary")
    total_words = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM vocabulary WHERE is_favorite = 1")
    total_favorites = c.fetchone()[0]

    conn.close()

    return render_template(
        "vocabulary.html",
        words=words,
        categories=categories,
        current_category=category,
        search_query=search,
        favorites_only=favorites_only,
        total_words=total_words,
        total_favorites=total_favorites
    )

@vocabulary_bp.route("/flashcards")
def flashcards():
    category = request.args.get("category", "")
    conn = get_db_connection()
    c = conn.cursor()

    query = "SELECT * FROM vocabulary WHERE 1=1"
    params = []
    if category:
        query += " AND category = ?"
        params.append(category)

    c.execute(query, params)
    words = [dict(row) for row in c.fetchall()]

    c.execute("SELECT DISTINCT category FROM vocabulary ORDER BY category ASC")
    categories = [row["category"] for row in c.fetchall()]
    conn.close()

    return render_template(
        "flashcards.html",
        words=words,
        categories=categories,
        current_category=category
    )

@vocabulary_bp.route("/favorite", methods=["POST"])
def toggle_favorite():
    data = request.get_json() or {}
    word_id = data.get("id")
    if not word_id:
        return jsonify({"error": "Missing word id"}), 400

    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT is_favorite FROM vocabulary WHERE id = ?", (word_id,))
    row = c.fetchone()
    if not row:
        conn.close()
        return jsonify({"error": "Word not found"}), 404

    new_fav = 0 if row["is_favorite"] == 1 else 1
    c.execute("UPDATE vocabulary SET is_favorite = ? WHERE id = ?", (new_fav, word_id))
    conn.commit()
    conn.close()

    return jsonify({"success": True, "word_id": word_id, "is_favorite": bool(new_fav)})
