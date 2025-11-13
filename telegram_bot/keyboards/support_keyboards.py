# 📄 /keyboards/support_keyboards.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# 🔹 کیبورد پشتیبانی (برای کاربران قفل و آزاد)
def support_menu(lang: str):
    if lang == "fa":
        buttons = [
            [KeyboardButton("📨 ارسال پیام به پشتیبانی")],
            [KeyboardButton("🔙 بازگشت"), KeyboardButton("🏠 منوی اصلی")]
        ]
    else:
        buttons = [
            [KeyboardButton("📨 Contact Support")],
            [KeyboardButton("🔙 Back"), KeyboardButton("🏠 Main Menu")]
        ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
