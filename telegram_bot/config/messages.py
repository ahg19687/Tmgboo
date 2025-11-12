# telegram_bot/config/messages.py
# message manager: choose language pack and provide get_text(key, **fmt)

import json, os
from pathlib import Path

BASE = Path(__file__).resolve().parent
DEFAULT_LANG = os.getenv("DEFAULT_LANG", "fa")

def load_pack(lang):
    path = BASE / f"texts_{lang}.json"
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

_packs = {
    "fa": load_pack("fa"),
    "en": load_pack("en")
}

def get_text(key, lang=None, **fmt):
    if not lang:
        lang = DEFAULT_LANG
    pack = _packs.get(lang, _packs["fa"])
    txt = pack.get(key) or _packs["fa"].get(key) or key
    return txt.format(**fmt) if fmt else txt
