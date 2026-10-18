-- LinguaMate AI Database Schema
-- Capstone 4: AI Language Learning Companion for Beginners

CREATE TABLE IF NOT EXISTS lessons (
    day_number INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    topic TEXT NOT NULL,
    level TEXT DEFAULT 'Beginner (A1)',
    grammar_focus TEXT NOT NULL,
    completed INTEGER DEFAULT 0,
    completed_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS vocabulary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word TEXT NOT NULL UNIQUE,
    part_of_speech TEXT NOT NULL,
    tamil_meaning TEXT NOT NULL,
    pronunciation_tip TEXT,
    category TEXT NOT NULL,
    level TEXT DEFAULT 'A1',
    example_sentence TEXT NOT NULL,
    example_tamil TEXT NOT NULL,
    is_favorite INTEGER DEFAULT 0,
    mastered INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS quiz_attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT DEFAULT 'Comprehensive',
    total_questions INTEGER NOT NULL,
    answered_questions INTEGER DEFAULT 0,
    score INTEGER NOT NULL,
    percentage REAL NOT NULL,
    is_completed INTEGER DEFAULT 1,
    details_json TEXT,
    attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS conversation_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    topic TEXT NOT NULL,
    sender TEXT NOT NULL, -- 'user' or 'ai'
    message TEXT NOT NULL,
    corrected_message TEXT,
    tamil_explanation TEXT,
    simpler_sentence TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS mistake_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL, -- 'grammar_checker', 'conversation', 'quiz'
    original_sentence TEXT NOT NULL,
    corrected_sentence TEXT NOT NULL,
    mistake_category TEXT NOT NULL,
    error_type TEXT DEFAULT 'grammar_mistake', -- 'grammar_mistake', 'quiz_incorrect'
    explanation_en TEXT,
    explanation_ta TEXT,
    reviewed INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_mistake_log_dedup 
ON mistake_log (original_sentence, corrected_sentence, mistake_category);


CREATE TABLE IF NOT EXISTS ai_comparisons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sentence_id INTEGER UNIQUE,
    sentence TEXT NOT NULL,
    expected_correction TEXT NOT NULL,
    target_rule TEXT NOT NULL,
    chatgpt_output TEXT,
    chatgpt_status TEXT DEFAULT 'Uncertain',
    gemini_output TEXT,
    gemini_status TEXT DEFAULT 'Uncertain',
    claude_output TEXT,
    claude_status TEXT DEFAULT 'Uncertain',
    human_verified_notes TEXT,
    verification_status TEXT DEFAULT 'Pending Review',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS user_progress (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS questionable_reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    module TEXT NOT NULL,
    input_text TEXT NOT NULL,
    ai_response TEXT,
    issue_category TEXT NOT NULL,
    user_notes TEXT,
    reported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
