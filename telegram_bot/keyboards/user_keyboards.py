# telegram_bot/keyboards/user_keyboards.py
from telegram import ReplyKeyboardMarkup, KeyboardButton
from config.messages import get_text  # تغییر از get_message به get_text

def main_menu(lang: str = "fa"):
    """Main menu for regular users (locked)"""
    if lang == "fa":
        keyboard = [
            ["🔓 قفل‌گشایی", "💬 پشتیبانی"],
            ["🌐 تغییر زبان"]
        ]
    else:
        keyboard = [
            ["🔓 Unlock", "💬 Support"],
            ["🌐 Change Language"]
        ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

def unlocked_user_menu(lang: str = "fa"):
    """Menu for unlocked users - Full access"""
    if lang == "fa":
        keyboard = [
            ["👤 پروفایل", "📨 مدیریت پیام‌ها"],
            ["👥 مدیریت گروه‌ها", "⏰ یادآورها"],
            ["🌐 تغییر زبان", "💬 پشتیبانی"]
        ]
    else:
        keyboard = [
            ["👤 Profile", "📨 Messages Management"],
            ["👥 Groups Management", "⏰ Reminders"],
            ["🌐 Change Language", "💬 Support"]
        ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

def user_messages_menu(lang: str = "fa"):
    """Messages Management Menu for unlocked users"""
    if lang == "fa":
        keyboard = [
            ["⏰ زمان‌بندی ارسال", "🚀 ارسال فوری"],
            ["✅ گروه‌های انتخاب شده", "📨 پیام به ادمین"],
            ["🔙 بازگشت"]
        ]
    else:
        keyboard = [
            ["⏰ Schedule Send", "🚀 Instant Send"],
            ["✅ Selected Groups", "📨 Message to Admin"],
            ["🔙 Back"]
        ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

def user_groups_menu(lang: str = "fa"):
    """Groups Management Menu for unlocked users"""
    if lang == "fa":
        keyboard = [
            ["📋 لیست گروه‌های من", "➕ اضافه کردن گروه"],
            ["🗑 حذف گروه", "🔙 بازگشت"]
        ]
    else:
        keyboard = [
            ["📋 My Groups List", "➕ Add Group"],
            ["🗑 Remove Group", "🔙 Back"]
        ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

def language_menu(lang: str = "fa"):
    """Language Selection Menu"""
    if lang == "fa":
        keyboard = [
            ["🇮🇷 فارسی", "🇬🇧 English"],
            ["🔙 بازگشت", "🏠 منوی اصلی"]
        ]
    else:
        keyboard = [
            ["🇮🇷 فارسی", "🇬🇧 English"],
            ["🔙 Back", "🏠 Main Menu"]
        ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

def back_menu(lang: str = "fa"):
    """General Back Menu"""
    if lang == "fa":
        keyboard = [["🔙 بازگشت", "🏠 منوی اصلی"]]
    else:
        keyboard = [["🔙 Back", "🏠 Main Menu"]]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
