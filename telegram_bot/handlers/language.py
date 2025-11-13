# telegram_bot/handlers/language.py

from telegram import Update
from telegram.ext import ContextTypes
from config.messages import get_text
from utils.database import upsert_user, get_user

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = (context.args[0] if context.args else "fa")
    user_rec = get_user(user.id) or {}
    user_rec["lang"] = lang
    upsert_user(user.id, user_rec)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=get_text("start_welcome", lang=lang))
# --- ADD AFTER LANGUAGE CHANGE ---
users[str(user_id)]["lang"] = new_lang
save_json("telegram_bot/data/users.json", users)
