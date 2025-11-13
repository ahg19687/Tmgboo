# telegram_bot/handlers/navigation.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.database import get_user
from config.messages import get_text

async def go_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = get_user(update.effective_user.id) or {}
    lang = user_data.get("lang", "fa")
    locked = user_data.get("locked", True)

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
            [InlineKeyboardButton(get_text("back_to_main", lang=lang), callback_data="main_menu")],
        ]

    # اگر از پیام استفاده می‌کند (نه callback)
    if update.message:
        await update.message.reply_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:  # اگر از callback استفاده می‌کند
        await update.callback_query.edit_message_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
