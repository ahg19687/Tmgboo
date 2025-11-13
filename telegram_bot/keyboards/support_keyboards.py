# telegram_bot/keyboards/support_keyboards.py
from telegram import ReplyKeyboardMarkup, KeyboardButton

def support_menu(lang: str):
    if lang == "fa":
        keyboard = [
            [KeyboardButton("📨 ارسال پیام به پشتیبانی")],
            [KeyboardButton("🔙 بازگشت"), KeyboardButton("🏠 منوی اصلی")]
        ]
    else:
        keyboard = [
            [KeyboardButton("📨 Contact Support")],
            [KeyboardButton("🔙 Back"), KeyboardButton("🏠 Main Menu")]
        ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
