# telegram_bot/keyboards/support_keyboards.py

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_support_main_keyboard(lang: str = "fa"):
    """کیبورد اصلی پشتیبانی - برای منوی اصلی"""
    if lang == "fa":
        keyboard = [
            [InlineKeyboardButton("📞 تماس با پشتیبانی", callback_data="support")],
            [InlineKeyboardButton("🔙 بازگشت به منوی اصلی", callback_data="main_menu")]
        ]
    else:
        keyboard = [
            [InlineKeyboardButton("📞 Contact Support", callback_data="support")],
            [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")]
        ]
    return InlineKeyboardMarkup(keyboard)

def get_admins_list_keyboard(admins, lang: str = "fa"):
    """کیبورد لیست ادمین‌ها برای انتخاب"""
    keyboard = []
    
    for admin in admins:
        admin_id = admin['user_id']
        admin_name = admin.get('name', f'Admin {admin_id}')
        
        keyboard.append([
            InlineKeyboardButton(
                f"👤 {admin_name}", 
                callback_data=f"support_admin_{admin_id}"
            )
        ])
    
    # دکمه بازگشت
    back_text = "🔙 بازگشت" if lang == "fa" else "🔙 Back"
    keyboard.append([InlineKeyboardButton(back_text, callback_data="main_menu")])
    
    return InlineKeyboardMarkup(keyboard)

def get_support_cancel_keyboard(lang: str = "fa"):
    """کیبورد لغو در حین نوشتن پیام"""
    if lang == "fa":
        keyboard = [
            [InlineKeyboardButton("❌ لغو ارسال", callback_data="cancel_support")]
        ]
    else:
        keyboard = [
            [InlineKeyboardButton("❌ Cancel", callback_data="cancel_support")]
        ]
    return InlineKeyboardMarkup(keyboard)

def get_admin_management_keyboard(user_id: int, lang: str = "fa"):
    """کیبورد مدیریت برای ادمین (زیر پیام کاربر)"""
    if lang == "fa":
        keyboard = [
            [
                InlineKeyboardButton("📨 پاسخ", callback_data=f"reply_to_{user_id}"),
                InlineKeyboardButton("✅ انجام شد", callback_data=f"support_done_{user_id}")
            ],
            [
                InlineKeyboardButton("🚫 بلاک کاربر", callback_data=f"block_user_{user_id}"),
                InlineKeyboardButton("👁‍🗨 مشاهده پروفایل", callback_data=f"view_profile_{user_id}")
            ]
        ]
    else:
        keyboard = [
            [
                InlineKeyboardButton("📨 Reply", callback_data=f"reply_to_{user_id}"),
                InlineKeyboardButton("✅ Done", callback_data=f"support_done_{user_id}")
            ],
            [
                InlineKeyboardButton("🚫 Block User", callback_data=f"block_user_{user_id}"),
                InlineKeyboardButton("👁‍🗨 View Profile", callback_data=f"view_profile_{user_id}")
            ]
        ]
    return InlineKeyboardMarkup(keyboard)

def get_admin_reply_keyboard(user_id: int, lang: str = "fa"):
    """کیبورد پاسخ ادمین به کاربر"""
    if lang == "fa":
        keyboard = [
            [
                InlineKeyboardButton("📤 ارسال پاسخ", callback_data=f"send_reply_{user_id}"),
                InlineKeyboardButton("❌ لغو پاسخ", callback_data=f"cancel_reply_{user_id}")
            ]
        ]
    else:
        keyboard = [
            [
                InlineKeyboardButton("📤 Send Reply", callback_data=f"send_reply_{user_id}"),
                InlineKeyboardButton("❌ Cancel Reply", callback_data=f"cancel_reply_{user_id}")
            ]
        ]
    return InlineKeyboardMarkup(keyboard)

def get_support_success_keyboard(lang: str = "fa"):
    """کیبورد بعد از ارسال موفق پیام پشتیبانی"""
    if lang == "fa":
        keyboard = [
            [InlineKeyboardButton("✅ بازگشت به منوی اصلی", callback_data="main_menu")],
            [InlineKeyboardButton("📞 ارسال پیام دیگر", callback_data="support")]
        ]
    else:
        keyboard = [
            [InlineKeyboardButton("✅ Back to Main Menu", callback_data="main_menu")],
            [InlineKeyboardButton("📞 Send Another Message", callback_data="support")]
        ]
    return InlineKeyboardMarkup(keyboard)

def get_support_error_keyboard(lang: str = "fa"):
    """کیبورد هنگام خطا در ارسال پیام"""
    if lang == "fa":
        keyboard = [
            [InlineKeyboardButton("🔄 تلاش مجدد", callback_data="support")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="main_menu")]
        ]
    else:
        keyboard = [
            [InlineKeyboardButton("🔄 Try Again", callback_data="support")],
            [InlineKeyboardButton("🔙 Back", callback_data="main_menu")]
        ]
    return InlineKeyboardMarkup(keyboard)

# کیبوردهای قدیمی برای سازگاری با کدهای موجود
def support_menu(lang: str):
    """تابع قدیمی - برای سازگاری با کدهای موجود"""
    return get_support_main_keyboard(lang)
