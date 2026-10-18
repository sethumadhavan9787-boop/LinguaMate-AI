import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "linguamate-capstone-default-secret-key-3029")
    DATABASE_PATH = BASE_DIR / "instance" / "linguamate.db"
    DATA_DIR = BASE_DIR / "data"
    
    # AI Provider Settings
    AI_PROVIDER = os.getenv("AI_PROVIDER", "offline").lower()
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
    
    # Application settings
    APP_NAME = "LinguaMate AI — Language Learning Companion"
    APP_TAGLINE = "A Safe, Bilingual English Learning Companion for Tamil Speakers"
    VERSION = "1.0.0 (Capstone Edition)"
    
    # Learning defaults
    DAILY_GOAL_MINUTES = 20
    DEFAULT_LEVEL = "Beginner (A1)"
