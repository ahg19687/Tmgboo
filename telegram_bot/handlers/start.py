# telegram_bot/handlers/start.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, MessageHandler, filters
from config.messages import get_text
from utils.database import upsert_user, get_user, is_admin
from .navigation import go_back  # ✅ اضافه شد
import logging

LOG = logging.getLogger(__name__)

# -------------------------------------------
# 🔹 /start command
async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_data = get_user(user.id) or {}
    lang = user_data.get("lang") or "fa"

    # اگر کاربر ادمین باشد، همیشه آزاد باشد
    if is_admin(user.id):
        locked = False
    else:
        # اگر کاربر جدید باشد یا قفل باشد:
        locked = user_data.get("locked", True)

    # متن خوش‌آمد به زبان کاربر
    if locked:
        text = get_text("start_locked", lang=lang)
        keyboard = [
            [InlineKeyboardButton(get_text("menu_language", lang=lang), callback_data="lang")],
            [InlineKeyboardButton(get_text("menu_unlock", lang=lang), callback_data="unlock")],
            [InlineKeyboardButton(get_text("menu_support", lang=lang), callback_data="support")],
        ]
    else:
        text = get_text("start_unlocked", lang=lang)
        keyboard = [
            [InlineKeyboardButton(get_text("menu_language", lang=lang), callback_data="lang")],
            [InlineKeyboardButton(get_text("menu_my_groups", lang=lang), callback_data="my_groups")],
            [InlineKeyboardButton(get_text("menu_scheduler", lang=lang), callback_data="scheduler")],
            [InlineKeyboardButton(get_text("menu_send_now", lang=lang), callback_data="send_now")],
            [InlineKeyboardButton(get_text("menu_profile", lang=lang), callback_data="profile")],
            [InlineKeyboardButton("🏠 منوی اصلی", callback_data="main_menu")],
        ]

    upsert_user(user.id, {"user_id": user.id, "lang": lang, "locked": locked})
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# -------------------------------------------
# 🔹 ثبت هندلرهای بازگشت / منوی اصلی
def register_navigation_handlers(app):
    # Handles “Back” and “Main Menu” buttons in both languages
    app.add_handler(MessageHandler(filters.Regex("^(🔙|🏠|بازگشت|منوی اصلی)$"), go_back))
