# 📄 /keyboards/user_keyboards.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# 🔹 منوی اصلی کاربر آزاد
def main_menu(lang: str):
    if lang == "fa":
        buttons = [
            [KeyboardButton("📋 گروه‌های من")],
            [KeyboardButton("🕒 زمان‌بندی ارسال"), KeyboardButton("📦 بکاپ")],
            [KeyboardButton("🌐 تغییر زبان")]
        ]
    else:
        buttons = [
            [KeyboardButton("📋 My Groups")],
            [KeyboardButton("🕒 Schedule"), KeyboardButton("📦 Backup")],
            [KeyboardButton("🌐 Change Language")]
        ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

# 🔹 منوی قفل‌شده (کاربر هنوز اشتراک نداره)
def locked_menu(lang: str):
    if lang == "fa":
        buttons = [
            [KeyboardButton("🔓 قفل‌گشایی"), KeyboardButton("💬 پشتیبانی")],
            [KeyboardButton("🌐 تغییر زبان")]
        ]
    else:
        buttons = [
            [KeyboardButton("🔓 Unlock"), KeyboardButton("💬 Support")],
            [KeyboardButton("🌐 Change Language")]
        ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

# 🔹 منوی زبان
def language_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton("🇮🇷 فارسی"), KeyboardButton("🇬🇧 English")],
            [KeyboardButton("🏠 منوی اصلی / Main Menu")]
        ],
        resize_keyboard=True
    )

# 🔹 کیبورد بازگشت به منوی قبل یا اصلی (افزوده شده)
# Added: Back/Main buttons
def back_main_menu(lang: str):
    if lang == "fa":
        buttons = [
            [KeyboardButton("🔙 بازگشت"), KeyboardButton("🏠 منوی اصلی")]
        ]
    else:
        buttons = [
            [KeyboardButton("🔙 Back"), KeyboardButton("🏠 Main Menu")]
        ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
