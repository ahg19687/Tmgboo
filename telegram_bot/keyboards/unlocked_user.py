# telegram_bot/keyboards/unlocked_user.py
from telegram import ReplyKeyboardMarkup, KeyboardButton

def get_unlocked_keyboard(lang="fa"):
    if lang == "fa":
        keyboard = [
            [KeyboardButton("📋 گروه‌های من"), KeyboardButton("🕒 زمان‌بندی")],
            [KeyboardButton("💬 پشتیبانی"), KeyboardButton("🌐 تغییر زبان")],
            [KeyboardButton("🏠 منوی اصلی"), KeyboardButton("🔙 بازگشت")]
        ]
    else:
        keyboard = [
            [KeyboardButton("📋 My Groups"), KeyboardButton("🕒 Scheduler")],
            [KeyboardButton("💬 Support"), KeyboardButton("🌐 Change language")],
            [KeyboardButton("🏠 Main Menu"), KeyboardButton("🔙 Back")]
        ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
