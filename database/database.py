import sqlite3
import json
import os
from pathlib import Path
from config import Config

def get_db_connection():
    Config.DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    Config.DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    schema_path = Path(__file__).parent / "schema.sql"
    
    with get_db_connection() as conn:
        with open(schema_path, "r", encoding="utf-8") as f:
            conn.executescript(f.read())
        
        # Migrations for existing database columns
        c = conn.cursor()
        # 1. quiz_attempts migrations
        c.execute("PRAGMA table_info(quiz_attempts)")
        qa_cols = [row["name"] for row in c.fetchall()]
        if "answered_questions" not in qa_cols:
            c.execute("ALTER TABLE quiz_attempts ADD COLUMN answered_questions INTEGER DEFAULT 0")
        if "is_completed" not in qa_cols:
            c.execute("ALTER TABLE quiz_attempts ADD COLUMN is_completed INTEGER DEFAULT 1")
            
        # 2. mistake_log migrations & deduplication
        c.execute("PRAGMA table_info(mistake_log)")
        ml_cols = [row["name"] for row in c.fetchall()]
        if "error_type" not in ml_cols:
            c.execute("ALTER TABLE mistake_log ADD COLUMN error_type TEXT DEFAULT 'grammar_mistake'")

        # Deduplicate existing duplicate mistake logs, keeping the earliest entry
        c.execute("""
            DELETE FROM mistake_log 
            WHERE id NOT IN (
                SELECT MIN(id) FROM mistake_log GROUP BY source, original_sentence
            )
        """)
            
        conn.commit()
        
    seed_initial_data()

def log_mistake(source, original_sentence, corrected_sentence, mistake_category, 
                error_type="grammar_mistake", explanation_en="", explanation_ta="", conn=None):
    """
    Records a learning mistake or updates an existing pending record to prevent
    duplicate entries for the same question or sentence.
    """
    should_close = False
    if conn is None:
        conn = get_db_connection()
        should_close = True

    c = conn.cursor()
    # Check if this exact mistake from the same source already exists
    c.execute(
        "SELECT id, reviewed FROM mistake_log WHERE source = ? AND original_sentence = ?",
        (source, original_sentence)
    )
    existing = c.fetchone()

    if existing:
        # Update existing record if not reviewed or re-occurred
        c.execute("""
            UPDATE mistake_log 
            SET corrected_sentence = ?, mistake_category = ?, error_type = ?,
                explanation_en = ?, explanation_ta = ?, created_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (corrected_sentence, mistake_category, error_type, explanation_en, explanation_ta, existing["id"]))
    else:
        c.execute("""
            INSERT INTO mistake_log (
                source, original_sentence, corrected_sentence, mistake_category, 
                error_type, explanation_en, explanation_ta, reviewed
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, 0)
        """, (
            source, original_sentence, corrected_sentence, mistake_category,
            error_type, explanation_en, explanation_ta
        ))

    conn.commit()
    if should_close:
        conn.close()

def seed_initial_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Seed Lessons if empty
    cursor.execute("SELECT COUNT(*) FROM lessons")
    if cursor.fetchone()[0] == 0:
        lessons_file = Config.DATA_DIR / "lessons.json"
        if lessons_file.exists():
            with open(lessons_file, "r", encoding="utf-8") as f:
                lessons = json.load(f)
                for l in lessons:
                    cursor.execute("""
                        INSERT INTO lessons (day_number, title, topic, level, grammar_focus, completed)
                        VALUES (?, ?, ?, ?, ?, 0)
                    """, (l["day_number"], l["title"], l["topic"], l["level"], l["grammar_focus"]))
    
    # 2. Seed Vocabulary if empty
    cursor.execute("SELECT COUNT(*) FROM vocabulary")
    if cursor.fetchone()[0] == 0:
        vocab_file = Config.DATA_DIR / "vocabulary.json"
        if vocab_file.exists():
            with open(vocab_file, "r", encoding="utf-8") as f:
                words = json.load(f)
                for w in words:
                    cursor.execute("""
                        INSERT OR IGNORE INTO vocabulary 
                        (word, part_of_speech, tamil_meaning, pronunciation_tip, category, level, example_sentence, example_tamil, is_favorite, mastered)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0, 0)
                    """, (
                        w["word"], w["part_of_speech"], w["tamil_meaning"], 
                        w.get("pronunciation_tip", ""), w["category"], w.get("level", "A1"),
                        w["example_sentence"], w["example_tamil"]
                    ))

    # 3. Seed AI Comparisons if empty
    cursor.execute("SELECT COUNT(*) FROM ai_comparisons")
    if cursor.fetchone()[0] == 0:
        comp_file = Config.DATA_DIR / "comparison_sentences.json"
        if comp_file.exists():
            with open(comp_file, "r", encoding="utf-8") as f:
                sentences = json.load(f)
                for s in sentences:
                    cursor.execute("""
                        INSERT OR IGNORE INTO ai_comparisons 
                        (sentence_id, sentence, expected_correction, target_rule, 
                         chatgpt_output, chatgpt_status, gemini_output, gemini_status, 
                         claude_output, claude_status, human_verified_notes, verification_status)
                        VALUES (?, ?, ?, ?, ?, 'Accurate', ?, 'Accurate', ?, 'Accurate', ?, ?)
                    """, (
                        s["id"], s["sentence"], s["expected_correction"], s["target_rule"],
                        s["chatgpt_output"], s["gemini_output"], s["claude_output"],
                        s.get("human_reviewed_answer", ""), s.get("verification_status", "Verified")
                    ))
                    
    # 4. Seed user_progress defaults if empty
    cursor.execute("SELECT COUNT(*) FROM user_progress")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT OR IGNORE INTO user_progress (key, value) VALUES ('learning_streak', '3')")
        cursor.execute("INSERT OR IGNORE INTO user_progress (key, value) VALUES ('daily_minutes_today', '15')")
        cursor.execute("INSERT OR IGNORE INTO user_progress (key, value) VALUES ('user_level', 'Beginner (A1)')")
        cursor.execute("INSERT OR IGNORE INTO user_progress (key, value) VALUES ('daily_goal_minutes', '20')")
        
    # 5. Seed some initial mistake log items for immediate user review
    cursor.execute("SELECT COUNT(*) FROM mistake_log")
    if cursor.fetchone()[0] == 0:
        initial_mistakes = [
            ("grammar_checker", "Myself Suresh, I am living in Salem.", "I am Suresh, and I live in Salem.", "L1 Transfer & Reflexive Pronoun", "Do not start self-introductions with 'Myself'.", "உங்களை அறிமுகப்படுத்தும் போது 'Myself' கூறக் கூடாது. 'I am' என்று கூற வேண்டும்.", 0),
            ("conversation", "She do not like tea.", "She does not like tea.", "Subject-Verb Agreement", "Singular third person requires 'does not'.", "'She' ஒருமை என்பதால் 'does not' வர வேண்டும்.", 1),
            ("quiz", "One of my friend is a software engineer.", "One of my friends is a software engineer.", "Concord (Plural after 'One of')", "Use plural noun after 'one of my'.", "'One of my' அடுத்து 'friends' என பன்மை வர வேண்டும்.", 0)
        ]
        for m in initial_mistakes:
            cursor.execute("""
                INSERT INTO mistake_log (source, original_sentence, corrected_sentence, mistake_category, explanation_en, explanation_ta, reviewed)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, m)
            
    conn.commit()
    conn.close()

# Database query helper functions
def get_dashboard_metrics():
    conn = get_db_connection()
    c = conn.cursor()
    
    # Completed lessons
    c.execute("SELECT COUNT(*) FROM lessons WHERE completed = 1")
    completed_lessons = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM lessons")
    total_lessons = c.fetchone()[0] or 14
    
    # Vocabulary learned / mastered
    c.execute("SELECT COUNT(*) FROM vocabulary")
    total_vocab = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM vocabulary WHERE is_favorite = 1")
    favorited_vocab = c.fetchone()[0]
    
    # Quiz scores: distinguish completed quizzes from incomplete/started
    c.execute("SELECT COUNT(*) FROM quiz_attempts")
    total_quizzes = c.fetchone()[0]

    # Completed attempts (where is_completed = 1 or answered_questions >= total_questions)
    c.execute("""
        SELECT AVG(percentage), COUNT(*) 
        FROM quiz_attempts 
        WHERE is_completed = 1 OR answered_questions >= total_questions
    """)
    comp_quiz_row = c.fetchone()
    completed_quizzes = comp_quiz_row[1] if comp_quiz_row else 0
    avg_quiz_score = round(comp_quiz_row[0], 1) if (comp_quiz_row and comp_quiz_row[0] is not None) else None
    
    # Streak & level
    c.execute("SELECT value FROM user_progress WHERE key = 'learning_streak'")
    streak_row = c.fetchone()
    streak = int(streak_row[0]) if streak_row else 3
    
    c.execute("SELECT value FROM user_progress WHERE key = 'user_level'")
    level_row = c.fetchone()
    user_level = level_row[0] if level_row else "Beginner (A1)"

    c.execute("SELECT value FROM user_progress WHERE key = 'daily_minutes_today'")
    today_min_row = c.fetchone()
    today_minutes = int(today_min_row[0]) if today_min_row else 15

    # Mistakes count
    c.execute("SELECT COUNT(*) FROM mistake_log WHERE reviewed = 0")
    pending_mistakes = c.fetchone()[0]

    conn.close()
    return {
        "completed_lessons": completed_lessons,
        "total_lessons": total_lessons,
        "lesson_percentage": round((completed_lessons / total_lessons) * 100, 1),
        "total_vocab": total_vocab,
        "favorited_vocab": favorited_vocab,
        "avg_quiz_score": avg_quiz_score,
        "total_quizzes": total_quizzes,
        "completed_quizzes": completed_quizzes,
        "streak": streak,
        "user_level": user_level,
        "today_minutes": today_minutes,
        "daily_goal": Config.DAILY_GOAL_MINUTES,
        "pending_mistakes": pending_mistakes
    }
