import os
from flask import Flask, render_template
from config import Config
from database.database import init_db
from ai.provider_adapters import get_ai_adapter

from routes import (
    dashboard_bp,
    lessons_bp,
    conversation_bp,
    vocabulary_bp,
    grammar_bp,
    quiz_bp,
    pronunciation_bp,
    comparison_bp,
    mistakes_bp,
    poster_bp,
    prompts_bp,
    reports_bp,
    responsible_ai_bp
)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize SQLite database and seed initial data
    with app.app_context():
        init_db()

    # Register blueprints
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(lessons_bp)
    app.register_blueprint(conversation_bp)
    app.register_blueprint(vocabulary_bp)
    app.register_blueprint(grammar_bp)
    app.register_blueprint(quiz_bp)
    app.register_blueprint(pronunciation_bp)
    app.register_blueprint(comparison_bp)
    app.register_blueprint(mistakes_bp)
    app.register_blueprint(poster_bp)
    app.register_blueprint(prompts_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(responsible_ai_bp)

    @app.context_processor
    def inject_global_context():
        adapter = get_ai_adapter()
        return {
            "app_name": Config.APP_NAME,
            "app_tagline": Config.APP_TAGLINE,
            "version": Config.VERSION,
            "ai_provider_name": adapter.name,
            "is_ai_available": adapter.is_available()
        }

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def internal_error(e):
        return render_template("500.html"), 500

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)
