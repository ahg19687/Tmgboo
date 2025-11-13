# 📄 /keyboards/code_keyboards.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# 🔹 منوی وارد کردن کد اشتراک
def code_entry_menu(lang: str):
    if lang == "fa":
        buttons = [
            [KeyboardButton("🔐 ارسال کد قفل‌گشایی")],
            [KeyboardButton("🔙 بازگشت"), KeyboardButton("🏠 منوی اصلی")]
        ]
    else:
        buttons = [
            [KeyboardButton("🔐 Send Unlock Code")],
            [KeyboardButton("🔙 Back"), KeyboardButton("🏠 Main Menu")]
        ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
