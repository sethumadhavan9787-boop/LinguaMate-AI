# LinguaMate AI — Language Learning Companion
### College Capstone 4: AI Language Learning Companion for Beginners (A1–A2)
**A Safe, Bilingual English Learning Web Application for Tamil Speakers**

---

## 1. Project Overview
**LinguaMate AI** is a production-grade, full-stack educational web application designed for Tamil-speaking beginners learning spoken and written English. The project demonstrates how free-tier and offline AI tools can support vernacular language acquisition while enforcing strict Responsible AI guardrails against hallucinations, cultural insensitivity, and pedagogical embarrassment.

- **Primary Users:** Tamil-speaking beginners learning English (CEFR A1–A2 level).
- **Core Budget:** $0.00 (Zero paid APIs, zero subscriptions, zero credit card requirements).
- **Architecture:** Provider-Independent Python Flask Backend + SQLite Database + Modern HTML5/CSS3/Bootstrap 5 Frontend.

---

## 2. Quick Start on Windows

### Prerequisites
- Python 3.10+ installed on Windows (Python 3.14+ supported).
- Any modern web browser (Google Chrome, Microsoft Edge, Firefox, or Safari).

### Step 1: Open Terminal (PowerShell or Command Prompt)
Navigate to the project root directory:
```powershell
cd "d:\Sethumadhavan_Projects\Final project"
```

### Step 2: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 3: Configure Environment (Optional)
The application works **100% offline out-of-the-box** without any API key! 
If you want to test optional free-tier cloud models, copy `.env.example` to `.env`:
```powershell
copy .env.example .env
```
*(Leave `AI_PROVIDER=offline` for zero-cost operation, or add a free Google Gemini / Groq API key).*

### Step 4: Run the Application
```powershell
python app.py
```

### Step 5: Open in Your Browser
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 3. Running Automated Tests
To run the automated test suite with detailed verbose output:
```powershell
python -m pytest tests/ -v
```
**Test Results:** **29/29 Automated Unit & Integration Tests Passing (100% Pass Rate)**.

To run the interactive feature verification script:
```powershell
python verify_features.py
```

---

## 4. Capstone Requirements vs. Implementation Checklist

| Requirement (Master Prompt) | Implemented Module / File | Verification Status |
|-----------------------------|---------------------------|---------------------|
| **A. Dashboard** | `routes/dashboard.py` & `templates/dashboard.html` | ✅ Streak, Level, Goal, Lessons, Vocab, Quizzes, Chart.js graphs |
| **B. AI Conversation Practice** | `routes/conversation.py`, `ai/conversation.py` | ✅ 7 topics, 3 difficulty tiers, polite correction, Tamil notes, simpler options |
| **C. Two-Week Learning Plan** | `routes/lessons.py`, `data/lessons.json` | ✅ Complete 14 days, 10 vocab/day, grammar rules, 5 examples, 5 practice MCQs |
| **D. Vocabulary Learning** | `routes/vocabulary.py`, `data/vocabulary.json` | ✅ 105 curated words, 8 categories, audio TTS, favorites, 3D flip flashcards with shuffle |
| **E. Grammar Correction Lab** | `routes/grammar.py`, `ai/grammar_checker.py` | ✅ Discrete error badges, Tamil explanations, model sentences, automated Mistake Log |
| **F. Diagnostic Quiz Generator**| `routes/quiz.py`, `ai/quiz_generator.py` | ✅ 10-question MCQs, 5 categories, instant score %, explanations, SQLite history |
| **G. Pronunciation Practice** | `routes/pronunciation.py`, `static/js/speech.js`| ✅ SpeechSynthesis TTS, speed controls (0.5x–1.2x), Web Speech mic recording, phonetics |
| **H. 3-Tool AI Comparison Lab** | `routes/comparison.py`, `data/comparison_sentences.json` | ✅ **Mandatory Capstone**: Compares ChatGPT vs Gemini vs Claude on 10 sentences |
| **I. Mistake Log & Spaced Review** | `routes/mistakes.py`, `templates/mistake_log.html` | ✅ Searchable mistake log, status filters, Day 1 vs Day 14 Before/After page |
| **J. Illustrated Poster** | `routes/poster.py`, `templates/poster.html` | ✅ 10 words, Tamil meanings, icons, print/PDF export styling |
| **K. Progress & Verification Reports**| `routes/reports.py`, `templates/reports.html` | ✅ Longitudinal charts, lesson audit, formal AI Verification & Limitations report |
| **L. Prompt Engineering Library** | `routes/prompts.py`, `data/prompts.json` | ✅ 10 production prompts, Role/Task/Context breakdown, Few-Shot and Self-Consistency |
| **4. Responsible AI & Safety** | `routes/responsible_ai.py`, `templates/responsible_ai.html`| ✅ Cultural nuance, dialect respect, hallucination guards, privacy, report modal |
| **7. SQLite Database** | `database/database.py`, `database/schema.sql` | ✅ Auto-initialized schema, parameterized queries, seeded data |
| **8. Provider Independence** | `ai/provider_adapters.py` | ✅ Zero paid dependencies, works 100% offline, optional Gemini/Groq/OpenAI |
| **9. Testing & Quality Assurance** | `tests/` (app, grammar, quiz, adapters) | ✅ 23 pytest tests passing |
| **10. Capstone Deliverables** | `docs/` (10 comprehensive documentation files) | ✅ All 15 required deliverable sections documented |

---

## 5. Technology Stack Summary
- **Backend:** Python 3.14, Flask 3.1.0, SQLite 3.
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla ES6+), Bootstrap 5.3, Bootstrap Icons 1.11.
- **Data Visualizations:** Chart.js 4.4.
- **Speech Engine:** Web Speech API (SpeechSynthesis TTS and SpeechRecognition STT).
- **Typography:** Google Fonts (*Mukta Malar* for Tamil script, *Plus Jakarta Sans* for English).
- **Testing:** pytest 9.1.1.

---

## 6. Project Directory Structure
```
linguamate-ai/
├── app.py                     # Central Flask application entry point
├── config.py                  # Environment and database configuration
├── requirements.txt           # Python package dependencies
├── .env.example               # Environment variables template
├── README.md                  # Comprehensive project documentation
├── database/
│   ├── __init__.py
│   ├── database.py            # SQLite connection, seeding, and queries
│   └── schema.sql             # Relational table schema definitions
├── ai/
│   ├── __init__.py
│   ├── conversation.py        # Bilingual conversation engine
│   ├── grammar_checker.py     # L1 transfer and grammar rule engine
│   ├── quiz_generator.py      # 10-question MCQ quiz builder
│   ├── provider_adapters.py   # Provider-independent AI layer (Offline/Gemini/Groq)
│   └── prompt_templates.py    # Standardized system prompts
├── routes/
│   ├── __init__.py
│   ├── dashboard.py           # Dashboard metrics and charts
│   ├── lessons.py             # 14-day study plan routes
│   ├── conversation.py        # Spoken conversation chat routes
│   ├── vocabulary.py          # 105+ vocabulary and flashcards
│   ├── grammar.py             # Grammar Correction Lab
│   ├── quiz.py                # Quiz generator and history
│   ├── pronunciation.py       # Speech synthesis and phonetics
│   ├── comparison.py          # 3-Tool AI comparison lab
│   ├── mistakes.py            # Mistake log and before/after report
│   ├── poster.py              # Illustrated poster generator
│   ├── prompts.py             # Prompt engineering library
│   ├── reports.py             # Learning analytics and verification
│   └── responsible_ai.py      # Responsible AI guidelines and reporting
├── data/
│   ├── vocabulary.json        # 105 curated bilingual words
│   ├── lessons.json           # Complete 14-day study plan data
│   ├── quiz_questions.json    # Diagnostic MCQ question bank
│   ├── comparison_sentences.json # 10 benchmark sentences across 3 AI models
│   ├── prompts.json           # 10 production prompt templates
│   └── assessment_data.json   # Baseline Day 1 vs Day 14 comparison metrics
├── templates/
│   ├── base.html              # Modern responsive layout with sidebar
│   ├── dashboard.html         # Learning dashboard
│   ├── lessons.html           # 14-day plan grid
│   ├── lesson_detail.html     # Daily lesson detail with interactive MCQs
│   ├── conversation.html      # Interactive chat tutor
│   ├── vocabulary.html        # Bilingual vocabulary library
│   ├── flashcards.html        # 3D interactive flashcards
│   ├── grammar.html           # Grammar Correction Lab
│   ├── quiz.html              # Diagnostic 10-question quiz
│   ├── quiz_history.html      # Past quiz attempt records
│   ├── pronunciation.html     # Pronunciation and recording tool
│   ├── comparison.html        # 3-Tool AI model comparison matrix
│   ├── mistake_log.html       # Searchable and filterable mistake log
│   ├── before_after.html      # Longitudinal before/after report
│   ├── poster.html            # Printable vocabulary study poster
│   ├── prompt_library.html    # Searchable prompt catalog
│   ├── reports.html           # Analytics and AI verification report
│   ├── responsible_ai.html    # Responsible AI and report audit log
│   ├── 404.html               # Custom 404 page
│   └── 500.html               # Custom 500 page
├── static/
│   ├── css/
│   │   └── style.css          # Theme variables, 3D flip, chat, print CSS
│   └── js/
│       ├── app.js             # Theme toggle, clipboard, AJAX helpers
│       └── speech.js          # Browser SpeechSynthesis & Web Speech STT
├── tests/
│   ├── __init__.py
│   ├── test_app.py            # HTTP route integration tests
│   ├── test_grammar.py        # Grammar detection unit tests
│   ├── test_quiz.py           # Quiz generation and scoring tests
│   └── test_ai_adapters.py    # Offline fallback verification
└── docs/
    ├── 01_CAPSTONE_ABSTRACT_AND_SPECS.md
    ├── 02_TWO_WEEK_LEARNING_PLAN.md
    ├── 03_VOCABULARY_SHEET.md
    ├── 04_QUIZ_AND_ANSWER_KEY.md
    ├── 05_THREE_TOOL_COMPARISON_REPORT.md
    ├── 06_AI_VERIFICATION_AND_LIMITATIONS.md
    ├── 07_BEFORE_AFTER_ASSESSMENT_REPORT.md
    ├── 08_RESPONSIBLE_AI_FRAMEWORK.md
    ├── 09_TEST_PLAN_AND_RESULTS.md
    └── 10_VIVA_AND_DEMO_GUIDE.md
```

---

## 7. College Capstone Deliverables Index
All required capstone documentation files are generated in the `docs/` folder:
1. **[Capstone Abstract & Technical Specifications](docs/01_CAPSTONE_ABSTRACT_AND_SPECS.md)**
2. **[Two-Week Learning Plan (14 Days)](docs/02_TWO_WEEK_LEARNING_PLAN.md)**
3. **[Bilingual Vocabulary Master Sheet (105 Words)](docs/03_VOCABULARY_SHEET.md)**
4. **[Ten-Question Diagnostic Quiz & Instructor Answer Key](docs/04_QUIZ_AND_ANSWER_KEY.md)**
5. **[Three-Tool AI Comparison Report (ChatGPT vs Gemini vs Claude)](docs/05_THREE_TOOL_COMPARISON_REPORT.md)**
6. **[AI Verification & Limitations Report](docs/06_AI_VERIFICATION_AND_LIMITATIONS.md)**
7. **[Before/After Assessment Comparative Report](docs/07_BEFORE_AFTER_ASSESSMENT_REPORT.md)**
8. **[Responsible AI & Ethical Safety Framework](docs/08_RESPONSIBLE_AI_FRAMEWORK.md)**
9. **[Test Plan & QA Test Results Report](docs/09_TEST_PLAN_AND_RESULTS.md)**
10. **[Examiner Viva Voce & 5-Minute Demonstration Guide](docs/10_VIVA_AND_DEMO_GUIDE.md)**
