# telegram_bot/handlers/start.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config.messages import get_text
from utils.database import upsert_user, get_user
import logging

LOG = logging.getLogger(__name__)

async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = (get_user(user.id) or {}).get("lang") or None
    text = get_text("start_welcome", lang=lang)
    keyboard = [
        [InlineKeyboardButton(get_text("menu_language", lang=lang), callback_data="lang")],
        [InlineKeyboardButton(get_text("menu_unlock", lang=lang), callback_data="unlock")],
        [InlineKeyboardButton(get_text("menu_support", lang=lang), callback_data="support")],
        [InlineKeyboardButton(get_text("menu_my_groups", lang=lang), callback_data="my_groups")],
        [InlineKeyboardButton(get_text("menu_scheduler", lang=lang), callback_data="scheduler")],
        [InlineKeyboardButton(get_text("menu_send_now", lang=lang), callback_data="send_now")],
        [InlineKeyboardButton(get_text("menu_profile", lang=lang), callback_data="profile")]
    ]
    upsert_user(user.id, {"user_id": user.id, "lang": lang or "fa"})
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=InlineKeyboardMarkup(keyboard))
# --- ADD THIS SECTION AT END OF start.py ---
from telegram.ext import MessageHandler, filters
from .navigation import go_back

def register_navigation_handlers(app):
    # Handles “Back” and “Main Menu” buttons in both languages
    app.add_handler(MessageHandler(filters.Regex("^(🔙|🏠|بازگشت|منوی اصلی)$"), go_back))
