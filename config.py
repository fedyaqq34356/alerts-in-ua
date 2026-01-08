import os
from dotenv import load_dotenv

load_dotenv()

ALERTS_API_TOKEN = os.getenv("ALERTS_API_TOKEN")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")
DNIPRO_UID = int(os.getenv("DNIPRO_UID", 332))
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 30))
LOG_FILE = os.getenv("LOG_FILE", "alert.log")

if not ALERTS_API_TOKEN or ALERTS_API_TOKEN == "YOUR_API_TOKEN_HERE":
    raise ValueError("Укажите ALERTS_API_TOKEN в .env")
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("Укажите TELEGRAM_BOT_TOKEN в .env")
if not TELEGRAM_CHANNEL_ID:
    raise ValueError("Укажите TELEGRAM_CHANNEL_ID в .env")