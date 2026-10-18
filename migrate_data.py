import sqlite3
import json
from database.database import init_db

# Ensure columns exist
init_db()

conn = sqlite3.connect('instance/linguamate.db')
c = conn.cursor()

# 1. Update quiz_attempts answered_questions and is_completed based on details_json
c.execute("SELECT id, total_questions, details_json FROM quiz_attempts")
attempts = c.fetchall()
for q_id, total, d_json in attempts:
    answered_count = 0
    if d_json:
        try:
            data = json.loads(d_json)
            answered_count = sum(1 for item in data if item.get('user_answer') is not None)
        except Exception:
            answered_count = 0
    is_completed = 1 if (answered_count >= total and total > 0) else 0
    c.execute(
        "UPDATE quiz_attempts SET answered_questions = ?, is_completed = ? WHERE id = ?",
        (answered_count, is_completed, q_id)
    )

print(f"Updated {len(attempts)} quiz attempt completion flags.")

# 2. Clean up mistake_log entries where source = 'quiz' and user choice was 'Not Answered'
c.execute("DELETE FROM mistake_log WHERE source = 'quiz' AND original_sentence LIKE '%(Your choice: Not Answered)%'")
deleted_unanswered = c.rowcount
print(f"Removed {deleted_unanswered} unanswered quiz placeholders from mistake_log.")

# 3. Label legitimate mistake entries with error_type
c.execute("UPDATE mistake_log SET error_type = 'quiz_incorrect' WHERE source = 'quiz'")
c.execute("UPDATE mistake_log SET error_type = 'grammar_mistake' WHERE source IN ('grammar_checker', 'conversation')")

conn.commit()
conn.close()
print("Migration and data cleanup completed successfully.")
