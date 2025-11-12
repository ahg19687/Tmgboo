# telegram_bot/utils/database.py
# JSON-backed database wrapper with simple API

import os
import json
from pathlib import Path
from threading import Lock
from config.database import load_datafile, save_datafile

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

_lock = Lock()
FILES = {
    "users": "users.json",
    "groups": "groups.json",
    "admins": "admins.json",
    "unlock_codes": "unlock_codes.json",
    "scheduled_messages": "scheduled_messages.json"
}

def _load(name):
    return load_datafile(FILES[name])

def _save(name, data):
    save_datafile(FILES[name], data)

# Users
def get_user(user_id):
    d = _load("users")
    return d.get(str(user_id))

def upsert_user(user_id, payload):
    d = _load("users")
    d[str(user_id)] = payload
    _save("users", d)

def list_users():
    d = _load("users")
    return [v for k,v in d.items()]

# Admins
def get_admins():
    d = _load("admins")
    return [v for k,v in d.items()]

def is_admin(user_id):
    d = _load("admins")
    return str(user_id) in d

def add_admin(user_id, level=2, visible=True):
    d = _load("admins")
    d[str(user_id)] = {"user_id": user_id, "level": level, "visible": visible}
    _save("admins", d)

def remove_admin(user_id):
    d = _load("admins")
    if str(user_id) in d:
        del d[str(user_id)]
        _save("admins", d)

# Groups
def add_group_for_user(owner_id, group_id, title=""):
    d = _load("groups")
    d[str(group_id)] = {"group_id": group_id, "owner_id": owner_id, "title": title, "active": True}
    _save("groups", d)
    # add to owner's list
    if owner_id:
        u = get_user(owner_id) or {"user_id": owner_id, "groups": []}
        u_groups = u.get("groups", [])
        if group_id not in u_groups:
            u_groups.append(group_id)
        u["groups"] = u_groups
        upsert_user(owner_id, u)

def list_groups():
    return [v for k,v in _load("groups").items()]

# Unlock codes
def load_unlock_codes():
    data = _load("unlock_codes")
    return data if isinstance(data, list) else []

def save_unlock_codes(listobj):
    _save("unlock_codes", listobj)

# Scheduled messages
def save_scheduled_message(obj):
    d = _load("scheduled_messages")
    import uuid
    id_ = obj.get("id") or str(uuid.uuid4())
    obj["id"] = id_
    d[id_] = obj
    _save("scheduled_messages", d)
    return id_

def list_scheduled_messages():
    return [v for k,v in _load("scheduled_messages").items()]
