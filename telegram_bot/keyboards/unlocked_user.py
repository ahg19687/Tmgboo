# telegram_bot/keyboards/unlocked_user.py
from telegram import ReplyKeyboardMarkup

def get_unlocked_keyboard(lang="fa"):
    if lang == "fa":
        keyboard = [
            ["📋 گروه‌های من", "🕒 زمان‌بندی"],
            ["💬 پشتیبانی", "🌐 تغییر زبان"],
            ["🏠 منوی اصلی"]
        ]
    else:
        keyboard = [
            ["📋 My Groups", "🕒 Scheduler"],
            ["💬 Support", "🌐 Change language"],
            ["🏠 Main Menu"]
        ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
