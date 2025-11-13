# telegram_bot/handlers/navigation.py

from telegram import Update
from telegram.ext import ContextTypes
from utils.database import get_user
from config.messages import get_text
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

async def go_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)
    lang = user.get("lang", "fa")
    locked = user.get("locked", True)

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
        ]

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
