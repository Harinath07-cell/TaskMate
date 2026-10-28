import os
from pathlib import Path
from dotenv import load_dotenv

# Locate base directory and load .env
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

class Config:
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    DEBUG = FLASK_ENV == "development"
    SECRET_KEY = os.getenv("SECRET_KEY", "taskmate-default-dev-secret-key-2026")
    PORT = int(os.getenv("FLASK_PORT", 5000))

    # MySQL Configuration
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "taskmate_db")
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")

    # SQLite Fallback for Local Dev / Testing if MySQL is unreachable
    DB_FALLBACK_SQLITE = os.getenv("DB_FALLBACK_SQLITE", "true").lower() in ("true", "1", "yes")
    _default_sqlite = "/tmp/taskmate_dev.db" if os.getenv("VERCEL") else str(BASE_DIR / "taskmate_dev.db")
    SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", _default_sqlite)

    # MongoDB Configuration
    MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/taskmate_logs")
    MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "taskmate_logs")

    # Groq AI Agent Configuration
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
    GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
    GROQ_FALLBACK_MODELS = ["openai/gpt-oss-120b", "openai/gpt-oss-20b", "llama-3.3-70b-versatile", "llama-3.1-8b-instant", "qwen/qwen3.8-27b"]
    GROQ_API_URL = os.getenv("GROQ_API_URL", "https://api.groq.com/openai/v1/chat/completions")
    GROQ_TIMEOUT = float(os.getenv("GROQ_TIMEOUT", "12.0"))

    # Optional Gemini AI Configuration (Fallback provider)
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
    AI_MODEL = os.getenv("AI_MODEL", "gemini-1.5-flash")

    # CORS Allowed Origins
    FRONTEND_ORIGIN = [
        origin.strip()
        for origin in os.getenv(
            "FRONTEND_ORIGIN",
            "http://localhost:5500,http://127.0.0.1:5500,http://localhost:5000,http://127.0.0.1:5000"
        ).split(",")
        if origin.strip()
    ]

    # Rate Limiting
    CHAT_RATE_LIMIT = int(os.getenv("CHAT_RATE_LIMIT", 30))

    # Vercel Services Internal Binding
    BACKEND_URL = os.getenv("BACKEND_URL", "").rstrip("/")
