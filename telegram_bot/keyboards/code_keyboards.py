# telegram_bot/keyboards/code_keyboards.py
from telegram import ReplyKeyboardMarkup, KeyboardButton

def code_entry_menu(lang: str):
    if lang == "fa":
        keyboard = [
            [KeyboardButton("🔐 ارسال کد قفل‌گشایی")],
            [KeyboardButton("🔙 بازگشت"), KeyboardButton("🏠 منوی اصلی")]
        ]
    else:
        keyboard = [
            [KeyboardButton("🔐 Send Unlock Code")],
            [KeyboardButton("🔙 Back"), KeyboardButton("🏠 Main Menu")]
        ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
