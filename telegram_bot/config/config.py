# telegram_bot/config/config.py
# fallback loader for settings.json

import os
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
SETTINGS_PATH = BASE / "settings.json"

def load_settings():
    try:
        with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        # fallback defaults
        return {
            "bot_token": os.getenv("BOT_TOKEN"),
            "default_lang": "fa",
            "delay_min_seconds": 2,
            "delay_max_seconds": 5,
            "batch_size": 30,
            "reminder_days_before_expiry": [7,1],
            "admin_main_id": os.getenv("ADMIN_ID"),
            "daily_send_time": "09:00",
            "backup_every_days": 7,
            "store_scheduled_texts": True,
            "db_engine": os.getenv("DB_ENGINE","json"),
            "app_mode": os.getenv("APP_MODE","production"),
            "log_level": os.getenv("LOG_LEVEL","INFO"),
            "rate_limit_per_minute": 60
        }

SETTINGS = load_settings()
