# telegram_bot/keyboards/admin_keyboards.py
from telegram import ReplyKeyboardMarkup, KeyboardButton

def admin_main_menu(lang: str):
    if lang == "fa":
        keyboard = [
            [KeyboardButton("➕ افزودن ادمین"), KeyboardButton("➖ حذف ادمین")],
            [KeyboardButton("🔑 ساخت کد اشتراک"), KeyboardButton("📋 گروه‌های کاربران")],
            [KeyboardButton("📨 پیام جمعی"), KeyboardButton("📦 بکاپ")],
            [KeyboardButton("🌐 تغییر زبان"), KeyboardButton("🔙 بازگشت")]
        ]
    else:
        keyboard = [
            [KeyboardButton("➕ Add Admin"), KeyboardButton("➖ Remove Admin")],
            [KeyboardButton("🔑 Generate Code"), KeyboardButton("📋 User Groups")],
            [KeyboardButton("📨 Broadcast"), KeyboardButton("📦 Backup")],
            [KeyboardButton("🌐 Change Language"), KeyboardButton("🔙 Back")]
        ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

def admin_back_menu(lang: str):
    if lang == "fa":
        keyboard = [[KeyboardButton("🔙 بازگشت"), KeyboardButton("🏠 منوی اصلی")]]
    else:
        keyboard = [[KeyboardButton("🔙 Back"), KeyboardButton("🏠 Main Menu")]]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
