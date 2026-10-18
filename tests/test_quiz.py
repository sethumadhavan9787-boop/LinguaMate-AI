import pytest
from ai.quiz_generator import QuizGenerator

@pytest.fixture
def quiz_gen():
    return QuizGenerator()

def test_generate_10_question_quiz(quiz_gen):
    questions = quiz_gen.generate_quiz(category="Comprehensive", count=10)
    assert len(questions) == 10
    for q in questions:
        assert "question" in q
        assert "options" in q
        assert len(q["options"]) == 4
        assert "correct_answer" in q
        assert "explanation_en" in q
        assert "explanation_ta" in q

def test_quiz_scoring_accuracy(quiz_gen):
    questions = [
        {"id": 1, "question": "Q1", "options": ["A", "B", "C", "D"], "correct_answer": 1},
        {"id": 2, "question": "Q2", "options": ["A", "B", "C", "D"], "correct_answer": 2}
    ]
    # Correct on first, wrong on second
    user_answers = {"1": 1, "2": 0}
    evaluation = quiz_gen.evaluate_quiz(questions, user_answers)

    assert evaluation["total_questions"] == 2
    assert evaluation["score"] == 1
    assert evaluation["percentage"] == 50.0
    assert evaluation["results"][0]["is_correct"] is True
    assert evaluation["results"][1]["is_correct"] is False

def test_mistake_log_deduplication():
    from database.database import get_db_connection, log_mistake
    conn = get_db_connection()
    c = conn.cursor()
    test_sentence = "Test Duplicate Question Error (Your choice: wrong)"
    
    # Delete any prior test data
    c.execute("DELETE FROM mistake_log WHERE original_sentence = ?", (test_sentence,))
    conn.commit()

    # Log the same mistake twice
    log_mistake("quiz", test_sentence, "Correct Answer", "Quiz (Grammar)", "quiz_incorrect", "Rule explanation", "Tamil explanation", conn=conn)
    log_mistake("quiz", test_sentence, "Correct Answer", "Quiz (Grammar)", "quiz_incorrect", "Rule explanation", "Tamil explanation", conn=conn)

    c.execute("SELECT COUNT(*) FROM mistake_log WHERE original_sentence = ?", (test_sentence,))
    count = c.fetchone()[0]
    assert count == 1, f"Expected 1 entry for duplicate question, found {count}"

    # Clean up test row
    c.execute("DELETE FROM mistake_log WHERE original_sentence = ?", (test_sentence,))
    conn.commit()
    conn.close()

