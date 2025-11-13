# telegram_bot/keyboards/locked_user.py
from telegram import ReplyKeyboardMarkup, KeyboardButton

def get_locked_keyboard(lang="fa"):
    if lang == "fa":
        keyboard = [
            [KeyboardButton("🔓 قفل‌گشایی"), KeyboardButton("💬 پشتیبانی")],
            [KeyboardButton("🌐 تغییر زبان")],
            [KeyboardButton("🔙 بازگشت"), KeyboardButton("🏠 منوی اصلی")]
        ]
    else:
        keyboard = [
            [KeyboardButton("🔓 Unlock"), KeyboardButton("💬 Support")],
            [KeyboardButton("🌐 Change language")],
            [KeyboardButton("🔙 Back"), KeyboardButton("🏠 Main Menu")]
        ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
