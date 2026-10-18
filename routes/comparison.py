import json
from flask import Blueprint, render_template, request, jsonify
from database.database import get_db_connection
from config import Config

comparison_bp = Blueprint("comparison", __name__, url_prefix="/comparison")

def load_predefined_comparisons():
    comp_file = Config.DATA_DIR / "comparison_sentences.json"
    if comp_file.exists():
        with open(comp_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

@comparison_bp.route("/")
def index():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM ai_comparisons ORDER BY sentence_id ASC")
    db_rows = {row["sentence_id"]: dict(row) for row in c.fetchall()}
    conn.close()

    raw_items = load_predefined_comparisons()
    items = []
    
    verified_count = 0
    uncertain_count = 0
    pending_count = 0

    for item in raw_items:
        s_id = item["id"]
        db_item = db_rows.get(s_id, {})
        
        merged = {
            "id": s_id,
            "sentence": item["sentence"],
            "target_rule": item["target_rule"],
            "expected_correction": item["expected_correction"],
            "tamil_context": item.get("tamil_context", ""),
            "chatgpt_output": db_item.get("chatgpt_output") or item.get("chatgpt_output", ""),
            "chatgpt_status": db_item.get("chatgpt_status", "Accurate"),
            "gemini_output": db_item.get("gemini_output") or item.get("gemini_output", ""),
            "gemini_status": db_item.get("gemini_status", "Accurate"),
            "claude_output": db_item.get("claude_output") or item.get("claude_output", ""),
            "claude_status": db_item.get("claude_status", "Accurate"),
            "google_translate": item.get("google_translate_crosscheck", ""),
            "common_pitfalls": item.get("common_ai_pitfalls", ""),
            "human_reviewed_answer": db_item.get("human_verified_notes") or item.get("human_reviewed_answer", ""),
            "verification_status": db_item.get("verification_status") or item.get("verification_status", "Verified")
        }
        
        status = merged["verification_status"].lower()
        if "verified" in status:
            verified_count += 1
        elif "uncertain" in status:
            uncertain_count += 1
        else:
            pending_count += 1
            
        items.append(merged)

    stats = {
        "total_test_sentences": len(items),
        "verified_count": verified_count,
        "uncertain_count": uncertain_count,
        "pending_count": pending_count,
        "models_compared": ["OpenAI ChatGPT", "Google Gemini", "Anthropic Claude"]
    }

    return render_template(
        "comparison.html",
        items=items,
        stats=stats
    )

@comparison_bp.route("/verify", methods=["POST"])
def update_verification():
    data = request.get_json() or {}
    sentence_id = data.get("sentence_id")
    status = data.get("status", "Verified")
    human_notes = data.get("human_notes", "").strip()
    chatgpt_out = data.get("chatgpt_output")
    gemini_out = data.get("gemini_output")
    claude_out = data.get("claude_output")

    if sentence_id is None:
        return jsonify({"error": "Missing sentence ID"}), 400

    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""
        UPDATE ai_comparisons 
        SET verification_status = ?, human_verified_notes = ?,
            chatgpt_output = COALESCE(?, chatgpt_output),
            gemini_output = COALESCE(?, gemini_output),
            claude_output = COALESCE(?, claude_output),
            updated_at = CURRENT_TIMESTAMP
        WHERE sentence_id = ?
    """, (status, human_notes, chatgpt_out, gemini_out, claude_out, sentence_id))
    conn.commit()
    conn.close()

    return jsonify({"success": True, "sentence_id": sentence_id, "status": status})

@comparison_bp.route("/add-custom", methods=["POST"])
def add_custom_sentence():
    data = request.get_json() or {}
    sentence = data.get("sentence", "").strip()
    rule = data.get("target_rule", "Custom Grammar Rule").strip()
    expected = data.get("expected_correction", "").strip()
    chatgpt = data.get("chatgpt_output", "").strip()
    gemini = data.get("gemini_output", "").strip()
    claude = data.get("claude_output", "").strip()
    notes = data.get("human_notes", "").strip()
    status = data.get("status", "Pending Review")

    if not sentence or not expected:
        return jsonify({"error": "Sentence and expected correction are required."}), 400

    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT MAX(sentence_id) FROM ai_comparisons")
    max_id = c.fetchone()[0] or 10
    new_id = max_id + 1

    c.execute("""
        INSERT INTO ai_comparisons 
        (sentence_id, sentence, expected_correction, target_rule,
         chatgpt_output, chatgpt_status, gemini_output, gemini_status,
         claude_output, claude_status, human_verified_notes, verification_status)
        VALUES (?, ?, ?, ?, ?, 'Manual Paste', ?, 'Manual Paste', ?, 'Manual Paste', ?, ?)
    """, (new_id, sentence, expected, rule, chatgpt, gemini, claude, notes, status))
    conn.commit()
    conn.close()

    return jsonify({"success": True, "sentence_id": new_id, "status": status})
