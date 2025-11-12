# telegram_bot/handlers/profile.py

from telegram import Update
from telegram.ext import ContextTypes
from utils.database import get_user
from utils.time_tools import remaining
from config.messages import get_text

async def profile_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    user_rec = get_user(uid) or {}
    sub = user_rec.get("subscription")
    if sub:
        rem = remaining(sub.get("expires_at"))
        rem_str = f"{rem['days']}d {rem['hours']}h"
    else:
        rem_str = "No subscription"
    groups = len(user_rec.get("groups", []))
    text = f"User: {uid}\nSubscription: {sub.get('type') if sub else '—'}\nRemaining: {rem_str}\nGroups: {groups}"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
