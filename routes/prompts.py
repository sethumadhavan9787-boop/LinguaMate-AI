import json
from flask import Blueprint, render_template, request
from config import Config

prompts_bp = Blueprint("prompts", __name__, url_prefix="/prompts")

def load_prompts():
    p_file = Config.DATA_DIR / "prompts.json"
    if p_file.exists():
        with open(p_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

@prompts_bp.route("/")
def index():
    category = request.args.get("category", "").strip()
    search = request.args.get("search", "").strip().lower()

    all_prompts = load_prompts()
    categories = sorted(list({p["category"] for p in all_prompts}))

    filtered = all_prompts
    if category:
        filtered = [p for p in filtered if p["category"] == category]

    if search:
        filtered = [
            p for p in filtered
            if search in p["title"].lower() 
            or search in p["purpose"].lower() 
            or search in p["prompt_text"].lower()
            or search in p["category"].lower()
        ]

    return render_template(
        "prompt_library.html",
        prompts=filtered,
        categories=categories,
        current_category=category,
        search_query=search,
        total_prompts=len(all_prompts)
    )
