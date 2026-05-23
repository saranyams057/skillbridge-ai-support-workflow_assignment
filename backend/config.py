import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.70"))
MAX_MESSAGES_BEFORE_SUMMARY = int(os.getenv("MAX_MESSAGES_BEFORE_SUMMARY", "12"))

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing. Add it to backend/.env")
