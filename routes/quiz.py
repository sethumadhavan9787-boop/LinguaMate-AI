import json
from flask import Blueprint, render_template, request, jsonify, session
from ai.quiz_generator import QuizGenerator
from ai.provider_adapters import get_ai_adapter
from database.database import get_db_connection, log_mistake

quiz_bp = Blueprint("quiz", __name__, url_prefix="/quiz")
adapter = get_ai_adapter()
quiz_gen = QuizGenerator(provider_adapter=adapter)

@quiz_bp.route("/")
def index():
    category = request.args.get("category", "Comprehensive")
    questions = quiz_gen.generate_quiz(category=category, count=10)
    
    # Store questions in session for grading
    session["current_quiz_questions"] = questions
    
    # Fetch user quiz history for progress display
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM quiz_attempts ORDER BY id DESC LIMIT 5")
    recent_attempts = [dict(row) for row in c.fetchall()]
    conn.close()

    categories = ["Comprehensive", "Vocabulary", "Grammar", "Translation", "Sentence Correction", "Conversation"]

    return render_template(
        "quiz.html",
        questions=questions,
        category=category,
        categories=categories,
        recent_attempts=recent_attempts,
        provider_name=adapter.name
    )

@quiz_bp.route("/submit", methods=["POST"])
def submit_quiz():
    data = request.get_json() or {}
    user_answers = data.get("answers", {})
    category = data.get("category", "Comprehensive")
    
    questions = session.get("current_quiz_questions")
    if not questions:
        # Fallback to regenerating
        questions = quiz_gen.generate_quiz(category=category, count=10)

    evaluation = quiz_gen.evaluate_quiz(questions, user_answers)

    # Save to SQLite database
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""
        INSERT INTO quiz_attempts (category, total_questions, answered_questions, score, percentage, is_completed, details_json)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        category,
        evaluation["total_questions"],
        evaluation.get("answered_questions", 0),
        evaluation["score"],
        evaluation["percentage"],
        1 if evaluation.get("is_completed", False) else 0,
        json.dumps(evaluation["results"], ensure_ascii=False)
    ))

    # Log only genuinely incorrect questions that were attempted (skip unanswered questions)
    letter_map = {"A": 0, "B": 1, "C": 2, "D": 3}
    for item in evaluation["results"]:
        u_ans = item.get("user_answer")
        # Only log if user actually provided an answer and it was incorrect
        if u_ans is not None and not item.get("is_correct"):
            options = item.get("options", [])
            c_ans = item.get("correct_answer")
            
            # Resolve user answer index
            u_idx = None
            if isinstance(u_ans, str) and u_ans.strip().upper() in letter_map:
                u_idx = letter_map[u_ans.strip().upper()]
            else:
                try:
                    u_idx = int(u_ans)
                except (ValueError, TypeError):
                    u_idx = None

            # Resolve correct answer index
            try:
                c_idx = int(c_ans) if c_ans is not None else 0
            except (ValueError, TypeError):
                c_idx = 0

            user_ans_text = options[u_idx] if (u_idx is not None and 0 <= u_idx < len(options)) else str(u_ans)
            correct_ans_text = options[c_idx] if (0 <= c_idx < len(options)) else ""
            
            # Log or update quiz mistake without creating duplicates
            log_mistake(
                source="quiz",
                original_sentence=f"Quiz Question: {item['question']} (Your choice: {user_ans_text})",
                corrected_sentence=f"Correct Answer: {correct_ans_text}",
                mistake_category=f"Quiz ({item.get('category', 'General')})",
                error_type="quiz_incorrect",
                explanation_en=item.get("explanation_en", ""),
                explanation_ta=item.get("explanation_ta", ""),
                conn=conn
            )

    conn.commit()
    conn.close()

    return jsonify({"success": True, "evaluation": evaluation})

@quiz_bp.route("/history")
def history():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM quiz_attempts ORDER BY id DESC LIMIT 20")
    attempts = [dict(row) for row in c.fetchall()]
    
    # Calculate stats (counting only completed quizzes for average score)
    c.execute("""
        SELECT AVG(percentage), MAX(percentage), COUNT(*) 
        FROM quiz_attempts 
        WHERE is_completed = 1 OR answered_questions >= total_questions
    """)
    comp_row = c.fetchone()
    avg_score = round(comp_row[0], 1) if (comp_row and comp_row[0] is not None) else 0.0
    best_score = round(comp_row[1], 1) if (comp_row and comp_row[1] is not None) else 0.0
    completed_attempts = comp_row[2] if comp_row else 0

    c.execute("SELECT COUNT(*) FROM quiz_attempts")
    total_attempts = c.fetchone()[0]
    
    conn.close()

    return render_template(
        "quiz_history.html",
        attempts=attempts,
        avg_score=avg_score,
        best_score=best_score,
        total_attempts=total_attempts,
        completed_attempts=completed_attempts
    )
