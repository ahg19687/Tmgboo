# telegram_bot/handlers/language.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config.messages import get_text
from utils.database import upsert_user, get_user

async def language_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش منوی انتخاب زبان"""
    user = update.effective_user
    user_data = get_user(user.id) or {}
    lang = user_data.get("lang", "fa")
    
    keyboard = [
        [InlineKeyboardButton("🇮🇷 فارسی", callback_data="setlang_fa")],
        [InlineKeyboardButton("🇺🇸 English", callback_data="setlang_en")],
        [InlineKeyboardButton(get_text("back_previous", lang=lang), callback_data="back_prev")],
        [InlineKeyboardButton(get_text("back_to_main", lang=lang), callback_data="main_menu")]
    ]
    
    await update.callback_query.edit_message_text(
        text=get_text("choose_language", lang=lang),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def set_language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """تغییر زبان از طریق callback"""
    query = update.callback_query
    await query.answer()
    
    user = update.effective_user
    lang = query.data.replace("setlang_", "")  # استخراج زبان از callback_data
    
    # ذخیره زبان کاربر
    user_data = get_user(user.id) or {}
    user_data["lang"] = lang
    upsert_user(user.id, user_data)
    
    await query.edit_message_text(
        text=get_text("lang_changed", lang=lang, lang=lang)
)
