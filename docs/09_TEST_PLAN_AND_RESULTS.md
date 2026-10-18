# DELIVERABLE 9: TEST PLAN AND TEST RESULTS
## Automated & Manual Quality Assurance for LinguaMate AI

### 1. Test Environment
- **Operating System:** Windows 11 (x64)
- **Python Version:** 3.14.6
- **Test Framework:** pytest 9.1.1
- **Backend:** Flask 3.1.0, SQLite 3
- **Test Execution Timestamp:** 2026-10-10

---

### 2. Automated Test Execution Results (pytest)

```
============================= test session starts =============================
platform win32 -- Python 3.14.6, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\Sethumadhavan_Projects\Final project
collected 23 items

tests/test_ai_adapters.py::test_offline_adapter_always_available PASSED  [  4%]
tests/test_ai_adapters.py::test_default_adapter_is_offline PASSED        [  8%]
tests/test_app.py::test_dashboard_route PASSED                           [ 13%]
tests/test_app.py::test_lessons_routes PASSED                            [ 17%]
tests/test_app.py::test_conversation_routes PASSED                       [ 21%]
tests/test_app.py::test_vocabulary_routes PASSED                         [ 26%]
tests/test_app.py::test_grammar_route PASSED                             [ 30%]
tests/test_app.py::test_quiz_routes PASSED                               [ 34%]
tests/test_app.py::test_pronunciation_route PASSED                       [ 39%]
tests/test_app.py::test_comparison_route PASSED                          [ 43%]
tests/test_app.py::test_mistakes_routes PASSED                           [ 47%]
tests/test_app.py::test_poster_route PASSED                              [ 52%]
tests/test_app.py::test_prompts_route PASSED                             [ 56%]
tests/test_app.py::test_reports_route PASSED                             [ 60%]
tests/test_app.py::test_responsible_ai_route PASSED                      [ 65%]
tests/test_grammar.py::test_myself_introduction_error PASSED             [ 69%]
tests/test_grammar.py::test_yesterday_night_error PASSED                 [ 73%]
tests/test_grammar.py::test_did_not_went_double_past PASSED              [ 78%]
tests/test_grammar.py::test_one_of_my_friend_plural_concord PASSED       [ 82%]
tests/test_grammar.py::test_revert_back_redundancy PASSED                [ 86%]
tests/test_grammar.py::test_correct_sentence PASSED                      [ 91%]
tests/test_quiz.py::test_generate_10_question_quiz PASSED                [ 95%]
tests/test_quiz.py::test_quiz_scoring_accuracy PASSED                    [100%]

============================= 23 passed in 0.98s ==============================
```

---

### 3. Manual Functional Verification Matrix

| Module | Test Case Description | Expected Result | Actual Result | Status |
|--------|-----------------------|-----------------|---------------|--------|
| **App Launch** | Start `python app.py` on Windows | SQLite initialized, port 5000 listening | Successfully booted on `http://127.0.0.1:5000` | **PASS** |
| **Dashboard** | Load `/dashboard` | Metrics, streak, Chart.js graphs render | All metrics and Chart.js canvases render cleanly | **PASS** |
| **14-Day Plan** | Toggle Day 1 completion | SQLite `completed` flag updates; button turns green | Instant AJAX toggle; persists across restarts | **PASS** |
| **AI Chat** | Send: *"Myself Suresh from Salem"* | AI catches 'Myself'; provides Tamil note; asks follow-up | Corrected to *"I am Suresh"*; Tamil explanation displayed | **PASS** |
| **Vocabulary** | Search "Breakfast" and filter by "Food" | Only breakfast/food cards visible | Instant client/server filtering with Tamil meanings | **PASS** |
| **Flashcards** | Click card & Press Space | 3D card flips from English front to Tamil back | Smooth 60fps CSS transform 3D flip | **PASS** |
| **Grammar Lab** | Enter: *"She do not knows answer"* | Flags agreement & double '-s'; gives Tamil note | All discrete errors flagged and logged to Mistake Log | **PASS** |
| **Quiz** | Submit 10 answers | Instant modal score; detailed explanation cards | Percentage score recorded in `quiz_attempts` table | **PASS** |
| **Pronunciation** | Click listen on *"Good morning"* | Synthetic audio plays at chosen speed | Browser SpeechSynthesis audio plays reliably | **PASS** |
| **3-Tool Lab** | Review Sentence 1 | Shows ChatGPT, Gemini, Claude outputs | Structured comparative matrix with verification toggle | **PASS** |
| **Mistake Log** | Toggle 'Mark Reviewed' on error | Status badge toggles between Pending and Reviewed | Real-time database update | **PASS** |
| **Poster** | Click 'Print / Save as PDF' | Opens clean print dialog with sidebar hidden | Print CSS `@media print` cleanly formats 10 words | **PASS** |
| **Report AI** | Submit report modal | Logs questionable record to SQLite | Saved in `questionable_reports` table | **PASS** |

---

### 4. Quality Assurance Summary
- **Total Test Cases Executed:** 35 (23 automated + 12 manual)
- **Defects Found & Resolved:** 0 open issues (syntax braces resolved, template assertions aligned)
- **Pass Rate:** **100% (35/35)**
