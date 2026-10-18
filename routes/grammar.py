from flask import Blueprint, render_template, request, jsonify
from ai.grammar_checker import GrammarChecker
from ai.provider_adapters import get_ai_adapter
from database.database import get_db_connection, log_mistake

grammar_bp = Blueprint("grammar", __name__, url_prefix="/grammar")
adapter = get_ai_adapter()
checker = GrammarChecker(provider_adapter=adapter)

SAMPLE_SENTENCES = [
    {"label": "Modal & Article Error", "sentence": "I will has book."},
    {"label": "Modal Verb Inflection", "sentence": "She will goes to school."},
    {"label": "Missing Article", "sentence": "She is teacher."},
    {"label": "Self-introduction Error", "sentence": "Myself Karthik, I am coming from Salem."},
    {"label": "Concord / One of Error", "sentence": "One of my friend is working in TCS company."},
    {"label": "Auxiliary Double Past", "sentence": "Yesterday night he did not went to college."},
    {"label": "Subject-Verb Agreement", "sentence": "She do not knows the correct answer."},
    {"label": "Stative Verb Transfer", "sentence": "I am having two brothers and one car."},
    {"label": "Uncountable Noun Error", "sentence": "He gave me a good advice yesterday."},
    {"label": "Double Conjunction Trap", "sentence": "Although he worked hard, but he failed."}
]

@grammar_bp.route("/")
def index():
    return render_template(
        "grammar.html",
        samples=SAMPLE_SENTENCES,
        provider_name=adapter.name
    )

@grammar_bp.route("/check", methods=["POST"])
def check_sentence():
    data = request.get_json() or {}
    sentence = data.get("sentence", "").strip()

    if not sentence:
        return jsonify({"error": "Please enter a sentence."}), 400

    result = checker.check_sentence(sentence)

    # If errors were found, automatically log to mistake_log in SQLite (preventing duplicates)
    if not result.get("is_correct", False) and result.get("errors"):
        log_mistake(
            source="grammar_checker",
            original_sentence=result.get("original", sentence),
            corrected_sentence=result.get("corrected", ""),
            mistake_category=result.get("mistake_category", ", ".join(result.get("errors", ["Grammar Mistake"]))),
            error_type="grammar_mistake",
            explanation_en=result.get("explanation_en") or result.get("confidence_note", "Identified by Grammar Lab"),
            explanation_ta=result.get("tamil_explanation", "")
        )

    return jsonify({"success": True, "result": result})
