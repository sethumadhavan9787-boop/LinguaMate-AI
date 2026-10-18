import pytest
from app import create_app
from database.database import init_db

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client

def test_dashboard_route(client):
    res = client.get("/")
    assert res.status_code == 200
    assert b"LinguaMate AI" in res.data
    assert b"Dashboard" in res.data
    assert b"progressChart" in res.data
    assert b"chartEmptyState" in res.data
    assert b"chart.js" in res.data

    # Test JSON chart endpoint
    res_api = client.get("/api/chart-data")
    assert res_api.status_code == 200
    data = res_api.get_json()
    assert data["success"] is True
    assert "quiz_history" in data


def test_lessons_routes(client):
    res = client.get("/lessons/")
    assert res.status_code == 200
    assert b"2-Week Study Plan" in res.data

    res_detail = client.get("/lessons/1")
    assert res_detail.status_code == 200
    assert b"Day 1: Greetings and Introductions" in res_detail.data

def test_conversation_routes(client):
    res = client.get("/conversation/")
    assert res.status_code == 200
    assert b"AI Conversation Partner" in res.data

    # Test send endpoint
    post_res = client.post("/conversation/send", json={
        "message": "Hello, my name is Priya.",
        "topic": "self_introduction",
        "level": "Beginner"
    })
    assert post_res.status_code == 200
    data = post_res.get_json()
    assert data["success"] is True
    assert "ai_response" in data["response"]

def test_vocabulary_routes(client):
    res = client.get("/vocabulary/")
    assert res.status_code == 200
    assert b"Bilingual Vocabulary Library" in res.data

    res_flash = client.get("/vocabulary/flashcards")
    assert res_flash.status_code == 200
    assert b"Interactive Flashcards" in res_flash.data

def test_grammar_route(client):
    res = client.get("/grammar/")
    assert res.status_code == 200
    assert b"Grammar Correction Lab" in res.data

    # Test POST /grammar/check with the bug case "i will has book"
    post_res = client.post("/grammar/check", json={"sentence": "i will has book"})
    assert post_res.status_code == 200
    data = post_res.get_json()
    assert data["success"] is True
    assert data["result"]["is_correct"] is False
    assert data["result"]["status"] == "Needs Correction"
    assert data["result"]["corrected"] == "I will have a book."
    assert "Modal Auxiliary & Base Verb" in data["result"]["errors"]
    assert "Missing Article / Determiner" in data["result"]["errors"]

def test_quiz_routes(client):
    res = client.get("/quiz/")
    assert res.status_code == 200
    assert b"10-Question Knowledge Check" in res.data

    res_hist = client.get("/quiz/history")
    assert res_hist.status_code == 200

def test_pronunciation_route(client):
    res = client.get("/pronunciation/")
    assert res.status_code == 200
    assert b"Pronunciation" in res.data
    assert b"Phonetics Lab" in res.data

def test_comparison_route(client):
    res = client.get("/comparison/")
    assert res.status_code == 200
    assert b"3-Tool AI Lab" in res.data
    assert b"ChatGPT" in res.data
    assert b"Gemini" in res.data
    assert b"Claude" in res.data

def test_mistakes_routes(client):
    res = client.get("/mistakes/")
    assert res.status_code == 200
    assert b"Mistake Log" in res.data

    res_ba = client.get("/mistakes/before-after")
    assert res_ba.status_code == 200
    assert b"Day 1 Diagnostic Baseline" in res_ba.data

def test_poster_route(client):
    res = client.get("/poster/")
    assert res.status_code == 200
    assert b"Illustrated Vocabulary Poster" in res.data

def test_prompts_route(client):
    res = client.get("/prompts/")
    assert res.status_code == 200
    assert b"Prompt Engineering Library" in res.data

def test_reports_route(client):
    res = client.get("/reports/")
    assert res.status_code == 200
    assert b"AI Verification" in res.data
    assert b"Limitations Report" in res.data

def test_responsible_ai_route(client):
    res = client.get("/responsible-ai/")
    assert res.status_code == 200
    assert b"Responsible AI" in res.data
    assert b"Safety Guidelines" in res.data

def test_vocabulary_toggle_favorite(client):
    res = client.post("/vocabulary/favorite", json={"id": 1})
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "is_favorite" in data
    # Toggle back to preserve baseline state
    client.post("/vocabulary/favorite", json={"id": 1})

def test_lessons_toggle_completion(client):
    res = client.post("/lessons/toggle-complete/1")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "completed" in data
    # Toggle back to preserve baseline state
    client.post("/lessons/toggle-complete/1")

def test_comparison_add_custom_sentence(client):
    res = client.post("/comparison/add-custom", json={
        "sentence": "He gave me a good advice.",
        "target_rule": "Uncountable Noun Error",
        "expected_correction": "He gave me a piece of good advice.",
        "chatgpt_output": "He gave me good advice.",
        "gemini_output": "He gave me a good piece of advice.",
        "claude_output": "He gave me some good advice.",
        "human_notes": "Advice is an uncountable noun in English; cannot take 'a advice'."
    })
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "sentence_id" in data

def test_quiz_submit_evaluation_flow(client):
    res = client.post("/quiz/submit", json={
        "category": "Vocabulary",
        "answers": {"0": 1, "1": 0, "2": 2}
    })
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "evaluation" in data
    assert "score" in data["evaluation"]
    assert "percentage" in data["evaluation"]
    assert "answered_questions" in data["evaluation"]

def test_mistake_review_toggle(client):
    res = client.post("/mistakes/toggle-review", json={"id": 1})
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "reviewed" in data
    # Toggle back to preserve baseline state
    client.post("/mistakes/toggle-review", json={"id": 1})

def test_dashboard_metrics_distinguishes_completed_quizzes(client):
    res = client.get("/dashboard")
    assert res.status_code == 200
    assert b"AVERAGE QUIZ SCORE" in res.data
    assert b"Live Analytics" in res.data

def test_dashboard_statistics_metrics(client):
    from database.database import get_dashboard_metrics
    metrics = get_dashboard_metrics()
    assert metrics["total_vocab"] == 105
    assert metrics["favorited_vocab"] >= 1
    assert metrics["total_lessons"] == 14
    assert metrics["lesson_percentage"] >= 0.0
    assert metrics["today_minutes"] == 15
    assert metrics["daily_goal"] == 20
    assert "total_quizzes" in metrics
    assert "completed_quizzes" in metrics
    # Verify average quiz score is computed or gracefully handled
    if metrics["completed_quizzes"] == 0:
        assert metrics["avg_quiz_score"] is None

def test_chart_data_api_and_zero_state(client):
    res = client.get("/api/chart-data")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "completed_count" in data
    assert "quiz_history" in data
    assert isinstance(data["quiz_history"], list)

def test_mistake_log_source_segregation(client):
    from database.database import get_db_connection, log_mistake
    conn = get_db_connection()
    c = conn.cursor()
    
    quiz_err = "Test sentence quiz mistake"
    grammar_err = "Test sentence grammar mistake"
    
    c.execute("DELETE FROM mistake_log WHERE original_sentence IN (?, ?)", (quiz_err, grammar_err))
    conn.commit()
    
    # Insert from quiz and grammar_checker
    log_mistake("quiz", quiz_err, "Corrected 1", "Quiz (Grammar)", "quiz_incorrect", "Eng 1", "Ta 1", conn=conn)
    log_mistake("grammar_checker", grammar_err, "Corrected 2", "Tense", "grammar_mistake", "Eng 2", "Ta 2", conn=conn)
    
    c.execute("SELECT source, error_type FROM mistake_log WHERE original_sentence = ?", (quiz_err,))
    row1 = c.fetchone()
    assert row1["source"] == "quiz"
    assert row1["error_type"] == "quiz_incorrect"
    
    c.execute("SELECT source, error_type FROM mistake_log WHERE original_sentence = ?", (grammar_err,))
    row2 = c.fetchone()
    assert row2["source"] == "grammar_checker"
    assert row2["error_type"] == "grammar_mistake"
    
    # Cleanup
    c.execute("DELETE FROM mistake_log WHERE original_sentence IN (?, ?)", (quiz_err, grammar_err))
    conn.commit()
    conn.close()




