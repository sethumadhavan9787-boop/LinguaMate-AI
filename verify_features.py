import sys
import io
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from app import create_app
from database.database import get_db_connection

app = create_app()
client = app.test_client()

print('=== 1. Testing Quiz Submission & SQLite Persistence ===')
with app.app_context():
    quiz_res = client.post('/quiz/submit', json={
        'category': 'Grammar',
        'answers': {'1': 'B', '2': 'C', '3': 'A', '4': 'D', '5': 'B'}
    })
    assert quiz_res.status_code == 200, f'Quiz submit failed: {quiz_res.status_code}'
    
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM quiz_attempts ORDER BY id DESC LIMIT 1')
        recent_quiz = c.fetchone()
    assert recent_quiz is not None, 'No quiz record saved in database'
    passed = (recent_quiz["percentage"] >= 60.0)
    print(f'Quiz persisted successfully: Score={recent_quiz["score"]}/{recent_quiz["total_questions"]}, Pct={recent_quiz["percentage"]}%, Passed={passed}')

print('=== 2. Testing AI Comparison Manual Entry Mode ===')
with app.app_context():
    comp_res = client.post('/comparison/add-custom', json={
        'sentence': 'I did not went to college yesterday.',
        'target_rule': 'Double Past Tense Avoidance',
        'expected_correction': 'I did not go to college yesterday.',
        'chatgpt_output': 'I did not go to college yesterday.',
        'gemini_output': 'I did not go to college yesterday.',
        'claude_output': 'I did not go to college yesterday.',
        'human_notes': 'Verified correct English syntax with base form of verb after did not.'
    })
    assert comp_res.status_code == 200, f'Comparison add-custom failed: {comp_res.status_code}'
    
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM ai_comparisons WHERE target_rule = ? ORDER BY id DESC LIMIT 1', ['Double Past Tense Avoidance'])
        recent_comp = c.fetchone()
    assert recent_comp is not None, 'Custom AI comparison was not saved to SQLite'
    print(f'Custom comparison persisted successfully: ID={recent_comp["id"]}, Sentence="{recent_comp["sentence"]}"')

print('=== 3. Testing Vocabulary Flashcards & Favorites ===')
with app.app_context():
    vocab_res = client.get('/vocabulary/flashcards')
    assert vocab_res.status_code == 200, f'Flashcards page failed: {vocab_res.status_code}'
    
    fav_res = client.post('/vocabulary/favorite', json={'id': 1})
    assert fav_res.status_code == 200, f'Favorite toggle failed: {fav_res.status_code}'
    fav_json = fav_res.get_json()
    print(f'Favorite toggle result: {fav_json}')

print('=== 4. Testing Grammar Correction via API ===')
with app.app_context():
    gram_res = client.post('/grammar/check', json={
        'sentence': 'Myself Rajesh and yesterday night I did not went there.'
    })
    assert gram_res.status_code == 200, f'Grammar check failed: {gram_res.status_code}'
    gram_json = gram_res.get_json()
    gram_data = gram_json.get("result", {})
    errors = gram_data.get("errors", [])
    print(f'Grammar check returned {len(errors)} error tags:')
    for err in errors:
        print(f'  - Tag: {err}')
    print(f'  - Corrected Sentence: "{gram_data.get("corrected")}"')
    print(f'  - Tamil Explanation: "{gram_data.get("tamil_explanation")}"')

print('=== 5. Testing Final Reports and Before/After Assessment ===')
with app.app_context():
    rep_res = client.get('/reports/', follow_redirects=True)
    assert rep_res.status_code == 200, f'Reports page failed: {rep_res.status_code}'
    
    ba_res = client.get('/mistakes/before-after', follow_redirects=True)
    assert ba_res.status_code == 200, f'Before-After page failed: {ba_res.status_code}'
    print('Reports and Before/After Assessment endpoints returned 200 OK.')

print('=== 6. Testing Printable Poster Route ===')
with app.app_context():
    poster_res = client.get('/poster/', follow_redirects=True)
    assert poster_res.status_code == 200, f'Poster page failed: {poster_res.status_code}'
    assert b'window.print()' in poster_res.data or b'print-btn' in poster_res.data
    print('Poster route returned 200 OK with print functionality.')

print('\n================ ALL INTEGRATION CHECKS PASSED (100%) ================')
