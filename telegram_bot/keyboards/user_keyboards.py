# telegram_bot/keyboards/user_keyboards.py
from telegram import ReplyKeyboardMarkup, KeyboardButton

def main_menu(lang: str):
    if lang == "fa":
        keyboard = [
            [KeyboardButton("📋 گروه‌های من")],
            [KeyboardButton("🕒 زمان‌بندی ارسال"), KeyboardButton("📦 بکاپ")],
            [KeyboardButton("🌐 تغییر زبان")],
            [KeyboardButton("🔙 بازگشت"), KeyboardButton("🏠 منوی اصلی")]
        ]
    else:
        keyboard = [
            [KeyboardButton("📋 My Groups")],
            [KeyboardButton("🕒 Schedule"), KeyboardButton("📦 Backup")],
            [KeyboardButton("🌐 Change Language")],
            [KeyboardButton("🔙 Back"), KeyboardButton("🏠 Main Menu")]
        ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

def locked_menu(lang: str):
    if lang == "fa":
        keyboard = [
            [KeyboardButton("🔓 قفل‌گشایی"), KeyboardButton("💬 پشتیبانی")],
            [KeyboardButton("🌐 تغییر زبان")],
            [KeyboardButton("🔙 بازگشت"), KeyboardButton("🏠 منوی اصلی")]
        ]
    else:
        keyboard = [
            [KeyboardButton("🔓 Unlock"), KeyboardButton("💬 Support")],
            [KeyboardButton("🌐 Change Language")],
            [KeyboardButton("🔙 Back"), KeyboardButton("🏠 Main Menu")]
        ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

def language_menu(lang: str = "fa"):
    if lang == "fa":
        keyboard = [
            [KeyboardButton("🇮🇷 فارسی"), KeyboardButton("🇬🇧 English")],
            [KeyboardButton("🔙 بازگشت"), KeyboardButton("🏠 منوی اصلی")]
        ]
    else:
        keyboard = [
            [KeyboardButton("🇮🇷 فارسی"), KeyboardButton("🇬🇧 English")],
            [KeyboardButton("🔙 Back"), KeyboardButton("🏠 Main Menu")]
        ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
