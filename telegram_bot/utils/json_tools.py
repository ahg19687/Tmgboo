# telegram_bot/utils/json_tools.py
# Utility for loading and saving JSON data safely

import json
import os
import logging

LOG = logging.getLogger(__name__)

def load_json(path: str, default=None):
    """Load JSON data from file, return default if file missing or corrupt."""
    if default is None:
        default = {}
    try:
        if not os.path.exists(path):
            return default
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        LOG.warning(f"Failed to load JSON {path}: {e}")
        return default

def save_json(path: str, data):
    """Save dictionary to JSON file (atomic and safe)."""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        tmp_path = path + ".tmp"
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, path)
        LOG.info(f"Saved JSON successfully → {path}")
    except Exception as e:
        LOG.error(f"Failed to save JSON {path}: {e}")
