# telegram_bot/config/database.py
# simple fallback DB loader for JSON files (used by utils/database)

import json, os
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "telegram_bot" / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

def load_datafile(name):
    path = DATA_DIR / name
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_datafile(name, data):
    path = DATA_DIR / name
    tmp = path.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)
