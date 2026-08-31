import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST") # e.g. https://bot1234.bothost.tech

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is missing in .env")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing in .env")
