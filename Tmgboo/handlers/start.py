from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from utils.translation import MESSAGES, LANG_LABEL
from utils.user_tools import ensure_user, is_active, load_users
from utils.ui_tools import inline_back_buttons, reply_start_keyboard
import os
async def handle_start(update: Update, context):
    user = update.effective_user
    ensure_user(user.id, user.username, user.first_name, user.last_name)
    users = load_users()
    lang = users.get(str(user.id), {}).get("lang", "fa")
    msgs = MESSAGES.get(lang, MESSAGES["fa"])
    kb = [
        [InlineKeyboardButton("🛠️ پشتیبانی / Support", callback_data="support")],
        [InlineKeyboardButton("🔐 قفل‌گشایی / Unlock", callback_data="unlock")],
        [InlineKeyboardButton(f"🌐 {LANG_LABEL.get(lang,'فارسی')}", callback_data="change_lang")]
    ]
    inline_kb = InlineKeyboardMarkup(kb + inline_back_buttons().keyboard)
    text = msgs["start_unlocked"] if is_active(user.id) else msgs["start_locked"]
    if update.message:
        await update.message.reply_text(text, reply_markup=inline_kb)
        await update.message.reply_text(" ", reply_markup=reply_start_keyboard())
    elif update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=inline_kb)
