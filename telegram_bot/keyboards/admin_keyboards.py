# telegram_bot/keyboards/admin_keyboards.py
from telegram import ReplyKeyboardMarkup, KeyboardButton
from config.messages import get_text  # تغییر از get_message به get_text

def admin_main_menu(lang: str = "fa"):
    """Admin Main Menu - Includes all management sections"""
    if lang == "fa":
        keyboard = [
            ["👤 مدیریت کاربران", "👥 مدیریت گروه‌ها"],
            ["🔑 مدیریت کدها", "⚙️ مدیریت ادمین‌ها"],
            ["📨 مدیریت پیام‌ها", "🌐 تغییر زبان"],
            ["🔙 بازگشت به منوی اصلی"]
        ]
    else:
        keyboard = [
            ["👤 User Management", "👥 Groups Management"],
            ["🔑 Codes Management", "⚙️ Admins Management"],
            ["📨 Messages Management", "🌐 Change Language"],
            ["🔙 Back to Main Menu"]
        ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

def admin_users_menu(lang: str = "fa"):
    """User Management Menu - List, Search, Promote, Lock/Unlock"""
    if lang == "fa":
        keyboard = [
            ["📋 لیست کاربران", "🔍 سرچ کاربران"],
            ["⬆️ ارتقا به ادمین درجه ۲", "⬆️ ارتقا به ادمین درجه ۱"],
            ["👤 مشاهده پروفایل کاربر", "📅 مشاهده اشتراک کاربر"],
            ["👥 لیست گروه‌های کاربر", "🔒 قفل کردن کاربر"],
            ["🔓 قفل‌گشایی کاربر", "📨 پیام‌های کاربر"],
            ["📤 پیام دادن به کاربر", "🔙 بازگشت"]
        ]
    else:
        keyboard = [
            ["📋 List Users", "🔍 Search Users"],
            ["⬆️ Promote to Admin Level 2", "⬆️ Promote to Admin Level 1"],
            ["👤 View User Profile", "📅 View User Subscription"],
            ["👥 User Groups List", "🔒 Lock User"],
            ["🔓 Unlock User", "📨 User Messages"],
            ["📤 Send Message to User", "🔙 Back"]
        ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

def admin_groups_menu(lang: str = "fa"):
    """Group Management Menu - List, Add, Remove"""
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

def admin_codes_menu(lang: str = "fa"):
    """Codes Management Menu - 5 different code types"""
    if lang == "fa":
        keyboard = [
            ["🧪 کد تست یک روزه", "📅 کد اشتراک ۱ ماهه"],
            ["📅 کد اشتراک ۳ ماهه", "📅 کد اشتراک ۴ ماهه"],
            ["🎁 کد هدیه", "📋 لیست کدهای فعال"],
            ["🔙 بازگشت"]
        ]
    else:
        keyboard = [
            ["🧪 1-Day Test Code", "📅 1-Month Subscription"],
            ["📅 3-Month Subscription", "📅 4-Month Subscription"],
            ["🎁 Gift Code", "📋 Active Codes List"],
            ["🔙 Back"]
        ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

def admin_admins_menu(lang: str = "fa"):
    """Admins Management Menu - List, Search, Add, Remove, Permissions"""
    if lang == "fa":
        keyboard = [
            ["📋 لیست ادمین‌ها", "🔍 سرچ ادمین‌ها"],
            ["➕ تنظیم ادمین جدید", "🗑 حذف ادمین"],
            ["⚙️ مدیریت دسترسی‌های ادمین", "📨 پیام‌های ادمین به من"],
            ["📤 پیام دادن به ادمین", "🔙 بازگشت"]
        ]
    else:
        keyboard = [
            ["📋 List Admins", "🔍 Search Admins"],
            ["➕ Add New Admin", "🗑 Remove Admin"],
            ["⚙️ Manage Admin Permissions", "📨 Admin Messages to Me"],
            ["📤 Send Message to Admin", "🔙 Back"]
        ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

def admin_messages_menu(lang: str = "fa"):
    """Messages Management Menu - Schedule, Instant Send, User Messages"""
    if lang == "fa":
        keyboard = [
            ["⏰ زمان‌بندی پیام", "🚀 ارسال پیام فوری"],
            ["📨 پیام به کاربر خاص", "✅ گروه‌های انتخاب شده"],
            ["🔙 بازگشت"]
        ]
    else:
        keyboard = [
            ["⏰ Schedule Message", "🚀 Instant Send"],
            ["📨 Message to Specific User", "✅ Selected Groups"],
            ["🔙 Back"]
        ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

def admin_back_menu(lang: str = "fa"):
    """Back Menu for Admin"""
    if lang == "fa":
        keyboard = [["🔙 بازگشت", "🏠 منوی اصلی ادمین"]]
    else:
        keyboard = [["🔙 Back", "🏠 Admin Main Menu"]]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
