# keyboards/admin_keyboards.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def admin_main_menu(lang: str = "fa"):
    """Admin Main Menu - Includes all management sections"""
    if lang == "fa":
        keyboard = [
            [InlineKeyboardButton("👤 مدیریت کاربران", callback_data="admin_users")],
            [InlineKeyboardButton("👥 مدیریت گروه‌ها", callback_data="admin_groups")],
            [InlineKeyboardButton("🔑 مدیریت کدها", callback_data="admin_codes")],
            [InlineKeyboardButton("⚙️ مدیریت ادمین‌ها", callback_data="admin_admins")],
            [InlineKeyboardButton("📨 مدیریت پیام‌ها", callback_data="admin_messages")],
            [InlineKeyboardButton("🌐 تغییر زبان", callback_data="admin_change_lang")],
            [InlineKeyboardButton("🔙 بازگشت به منوی اصلی", callback_data="main_menu")]
        ]
    else:
        keyboard = [
            [InlineKeyboardButton("👤 User Management", callback_data="admin_users")],
            [InlineKeyboardButton("👥 Groups Management", callback_data="admin_groups")],
            [InlineKeyboardButton("🔑 Codes Management", callback_data="admin_codes")],
            [InlineKeyboardButton("⚙️ Admins Management", callback_data="admin_admins")],
            [InlineKeyboardButton("📨 Messages Management", callback_data="admin_messages")],
            [InlineKeyboardButton("🌐 Change Language", callback_data="admin_change_lang")],
            [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")]
        ]
    return InlineKeyboardMarkup(keyboard)

def admin_users_menu(lang: str = "fa"):
    """User Management Menu - List, Search, Promote, Lock/Unlock"""
    if lang == "fa":
        keyboard = [
            [InlineKeyboardButton("📋 لیست کاربران", callback_data="admin_users_list")],
            [InlineKeyboardButton("🔍 سرچ کاربران", callback_data="admin_users_search")],
            [InlineKeyboardButton("⬆️ ارتقا به ادمین درجه ۲", callback_data="admin_promote_level2")],
            [InlineKeyboardButton("⬆️ ارتقا به ادمین درجه ۱", callback_data="admin_promote_level1")],
            [InlineKeyboardButton("👤 مشاهده پروفایل کاربر", callback_data="admin_view_profile")],
            [InlineKeyboardButton("📅 مشاهده اشتراک کاربر", callback_data="admin_view_subscription")],
            [InlineKeyboardButton("👥 لیست گروه‌های کاربر", callback_data="admin_user_groups")],
            [InlineKeyboardButton("🔒 قفل کردن کاربر", callback_data="admin_lock_user")],
            [InlineKeyboardButton("🔓 قفل‌گشایی کاربر", callback_data="admin_unlock_user")],
            [InlineKeyboardButton("📨 پیام‌های کاربر", callback_data="admin_user_messages")],
            [InlineKeyboardButton("📤 پیام دادن به کاربر", callback_data="admin_message_to_user")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="admin_main")]
        ]
    else:
        keyboard = [
            [InlineKeyboardButton("📋 List Users", callback_data="admin_users_list")],
            [InlineKeyboardButton("🔍 Search Users", callback_data="admin_users_search")],
            [InlineKeyboardButton("⬆️ Promote to Admin Level 2", callback_data="admin_promote_level2")],
            [InlineKeyboardButton("⬆️ Promote to Admin Level 1", callback_data="admin_promote_level1")],
            [InlineKeyboardButton("👤 View User Profile", callback_data="admin_view_profile")],
            [InlineKeyboardButton("📅 View User Subscription", callback_data="admin_view_subscription")],
            [InlineKeyboardButton("👥 User Groups List", callback_data="admin_user_groups")],
            [InlineKeyboardButton("🔒 Lock User", callback_data="admin_lock_user")],
            [InlineKeyboardButton("🔓 Unlock User", callback_data="admin_unlock_user")],
            [InlineKeyboardButton("📨 User Messages", callback_data="admin_user_messages")],
            [InlineKeyboardButton("📤 Send Message to User", callback_data="admin_message_to_user")],
            [InlineKeyboardButton("🔙 Back", callback_data="admin_main")]
        ]
    return InlineKeyboardMarkup(keyboard)

def admin_groups_menu(lang: str = "fa"):
    """Group Management Menu - List, Add, Remove"""
    if lang == "fa":
        keyboard = [
            [InlineKeyboardButton("📋 لیست گروه‌های من", callback_data="admin_groups_list")],
            [InlineKeyboardButton("➕ اضافه کردن گروه", callback_data="admin_add_group")],
            [InlineKeyboardButton("🗑 حذف گروه", callback_data="admin_remove_group")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="admin_main")]
        ]
    else:
        keyboard = [
            [InlineKeyboardButton("📋 My Groups List", callback_data="admin_groups_list")],
            [InlineKeyboardButton("➕ Add Group", callback_data="admin_add_group")],
            [InlineKeyboardButton("🗑 Remove Group", callback_data="admin_remove_group")],
            [InlineKeyboardButton("🔙 Back", callback_data="admin_main")]
        ]
    return InlineKeyboardMarkup(keyboard)

def admin_codes_menu(lang: str = "fa"):
    """Codes Management Menu - 5 different code types"""
    if lang == "fa":
        keyboard = [
            [InlineKeyboardButton("🧪 کد تست یک روزه", callback_data="admin_code_1day")],
            [InlineKeyboardButton("📅 کد اشتراک ۱ ماهه", callback_data="admin_code_1month")],
            [InlineKeyboardButton("📅 کد اشتراک ۳ ماهه", callback_data="admin_code_3month")],
            [InlineKeyboardButton("📅 کد اشتراک ۴ ماهه", callback_data="admin_code_4month")],
            [InlineKeyboardButton("🎁 کد هدیه", callback_data="admin_code_gift")],
            [InlineKeyboardButton("📋 لیست کدهای فعال", callback_data="admin_codes_list")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="admin_main")]
        ]
    else:
        keyboard = [
            [InlineKeyboardButton("🧪 1-Day Test Code", callback_data="admin_code_1day")],
            [InlineKeyboardButton("📅 1-Month Subscription", callback_data="admin_code_1month")],
            [InlineKeyboardButton("📅 3-Month Subscription", callback_data="admin_code_3month")],
            [InlineKeyboardButton("📅 4-Month Subscription", callback_data="admin_code_4month")],
            [InlineKeyboardButton("🎁 Gift Code", callback_data="admin_code_gift")],
            [InlineKeyboardButton("📋 Active Codes List", callback_data="admin_codes_list")],
            [InlineKeyboardButton("🔙 Back", callback_data="admin_main")]
        ]
    return InlineKeyboardMarkup(keyboard)

def admin_admins_menu(lang: str = "fa"):
    """Admins Management Menu - List, Search, Add, Remove, Permissions"""
    if lang == "fa":
        keyboard = [
            [InlineKeyboardButton("📋 لیست ادمین‌ها", callback_data="admin_admins_list")],
            [InlineKeyboardButton("🔍 سرچ ادمین‌ها", callback_data="admin_admins_search")],
            [InlineKeyboardButton("➕ تنظیم ادمین جدید", callback_data="admin_add_admin")],
            [InlineKeyboardButton("🗑 حذف ادمین", callback_data="admin_remove_admin")],
            [InlineKeyboardButton("⚙️ مدیریت دسترسی‌های ادمین", callback_data="admin_manage_permissions")],
            [InlineKeyboardButton("📨 پیام‌های ادمین به من", callback_data="admin_admin_messages")],
            [InlineKeyboardButton("📤 پیام دادن به ادمین", callback_data="admin_message_to_admin")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="admin_main")]
        ]
    else:
        keyboard = [
            [InlineKeyboardButton("📋 List Admins", callback_data="admin_admins_list")],
            [InlineKeyboardButton("🔍 Search Admins", callback_data="admin_admins_search")],
            [InlineKeyboardButton("➕ Add New Admin", callback_data="admin_add_admin")],
            [InlineKeyboardButton("🗑 Remove Admin", callback_data="admin_remove_admin")],
            [InlineKeyboardButton("⚙️ Manage Admin Permissions", callback_data="admin_manage_permissions")],
            [InlineKeyboardButton("📨 Admin Messages to Me", callback_data="admin_admin_messages")],
            [InlineKeyboardButton("📤 Send Message to Admin", callback_data="admin_message_to_admin")],
            [InlineKeyboardButton("🔙 Back", callback_data="admin_main")]
        ]
    return InlineKeyboardMarkup(keyboard)

def admin_messages_menu(lang: str = "fa"):
    """Messages Management Menu - Schedule, Instant Send, User Messages"""
    if lang == "fa":
        keyboard = [
            [InlineKeyboardButton("⏰ زمان‌بندی پیام", callback_data="admin_schedule_message")],
            [InlineKeyboardButton("🚀 ارسال پیام فوری", callback_data="admin_instant_send")],
            [InlineKeyboardButton("📨 پیام به کاربر خاص", callback_data="admin_message_to_user")],
            [InlineKeyboardButton("✅ گروه‌های انتخاب شده", callback_data="admin_selected_groups")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="admin_main")]
        ]
    else:
        keyboard = [
            [InlineKeyboardButton("⏰ Schedule Message", callback_data="admin_schedule_message")],
            [InlineKeyboardButton("🚀 Instant Send", callback_data="admin_instant_send")],
            [InlineKeyboardButton("📨 Message to Specific User", callback_data="admin_message_to_user")],
            [InlineKeyboardButton("✅ Selected Groups", callback_data="admin_selected_groups")],
            [InlineKeyboardButton("🔙 Back", callback_data="admin_main")]
        ]
    return InlineKeyboardMarkup(keyboard)

def admin_back_menu(lang: str = "fa"):
    """Back Menu for Admin"""
    if lang == "fa":
        keyboard = [
            [InlineKeyboardButton("🔙 بازگشت", callback_data="admin_back"),
             InlineKeyboardButton("🏠 منوی اصلی ادمین", callback_data="admin_main")]
        ]
    else:
        keyboard = [
            [InlineKeyboardButton("🔙 Back", callback_data="admin_back"),
             InlineKeyboardButton("🏠 Admin Main Menu", callback_data="admin_main")]
        ]
    return InlineKeyboardMarkup(keyboard)
