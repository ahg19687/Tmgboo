# telegram_bot/handlers/language.py

from telegram import Update
from telegram.ext import ContextTypes
from config.messages import get_text
from utils.database import upsert_user, get_user
from telegram_bot.utils.json_tools import save_json, load_json # اگر داری از فایل json_tools استفاده می‌کنی

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = (context.args[0] if context.args else "fa")

    # دریافت یا ایجاد رکورد کاربر
    user_rec = get_user(user.id) or {}
    user_rec["lang"] = lang
    upsert_user(user.id, user_rec)

    # --- ذخیره در فایل JSON در صورت نیاز ---
    try:
        users = load_json("telegram_bot/data/users.json")
        users[str(user.id)] = user_rec
        save_json("telegram_bot/data/users.json", users)
    except Exception as e:
        print(f"[language.py] Warning: could not save user data - {e}")

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=get_text("start_welcome", lang=lang)
    )
