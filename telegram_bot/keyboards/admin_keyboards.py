# 📄 /keyboards/admin_keyboards.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# 🔹 منوی اصلی ادمین
def admin_main_menu(lang: str):
    if lang == "fa":
        buttons = [
            [KeyboardButton("➕ افزودن ادمین"), KeyboardButton("➖ حذف ادمین")],
            [KeyboardButton("🔑 ساخت کد اشتراک"), KeyboardButton("📋 گروه‌های کاربران")],
            [KeyboardButton("📨 پیام جمعی"), KeyboardButton("📦 بکاپ")],
            [KeyboardButton("🌐 تغییر زبان"), KeyboardButton("🏠 منوی اصلی")]
        ]
    else:
        buttons = [
            [KeyboardButton("➕ Add Admin"), KeyboardButton("➖ Remove Admin")],
            [KeyboardButton("🔑 Generate Code"), KeyboardButton("📋 User Groups")],
            [KeyboardButton("📨 Broadcast"), KeyboardButton("📦 Backup")],
            [KeyboardButton("🌐 Change Language"), KeyboardButton("🏠 Main Menu")]
        ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

# 🔹 کیبورد بازگشت در صفحات ادمین (افزوده شده)
# Added: Back/Main buttons
def admin_back_main(lang: str):
    if lang == "fa":
        buttons = [[KeyboardButton("🔙 بازگشت"), KeyboardButton("🏠 منوی اصلی")]]
    else:
        buttons = [[KeyboardButton("🔙 Back"), KeyboardButton("🏠 Main Menu")]]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
