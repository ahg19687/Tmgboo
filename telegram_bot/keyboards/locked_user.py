# telegram_bot/keyboards/locked_user.py
from telegram import ReplyKeyboardMarkup

def get_locked_keyboard(lang="fa"):
    if lang == "fa":
        keyboard = [
            ["🔓 قفل‌گشایی", "💬 پشتیبانی"],
            ["🌐 تغییر زبان"]
        ]
    else:
        keyboard = [
            ["🔓 Unlock", "💬 Support"],
            ["🌐 Change language"]
        ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
