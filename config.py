import os
from dotenv import load_dotenv

# تحميل المتغيرات من ملف .env
load_dotenv()

# التحقق من مفتاح Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash").strip()

VOICE_LANGUAGE = os.getenv("VOICE_LANGUAGE", "ar-MA").strip()

try:
    VOICE_SECONDS = max(2, min(15, int(os.getenv("VOICE_SECONDS", "5"))))
except ValueError:
    VOICE_SECONDS = 5

try:
    TTS_RATE = int(os.getenv("TTS_RATE", "175"))
except ValueError:
    TTS_RATE = 175