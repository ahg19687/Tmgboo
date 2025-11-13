        # telegram_bot/handlers/misc_callbacks.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config.messages import get_text
from utils.database import get_user, upsert_user, is_admin
from keyboards.admin_keyboards import admin_main_menu, admin_users_menu, admin_groups_menu, admin_codes_menu, admin_admins_menu, admin_messages_menu
from keyboards.user_keyboards import unlocked_user_menu, user_messages_menu, user_groups_menu, main_menu
from keyboards.locked_user import get_locked_keyboard

# Import handlers
from .admin_users_handlers import admin_list_users, admin_search_user, admin_promote_user, admin_lock_user, admin_unlock_user
from .admin_codes_handlers import admin_generate_test_code, admin_generate_1month_code, admin_generate_3month_code, admin_generate_4month_code, admin_generate_gift_code
from .admin_admins_handlers import admin_list_admins, admin_add_admin, admin_remove_admin
from .admin_messages_handlers import admin_broadcast_message, admin_send_to_user
from .user_groups import groups_menu, list_groups_cmd, add_group_cmd
from .message_scheduler import scheduler_menu, send_now_menu
from .user_messages_handlers import user_instant_send, user_message_to_admin
from .profile import profile_cmd
from .support import get_support_message

async def callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    user = update.effective_user
    
    # گرفتن زبان کاربر
    user_data = get_user(user.id) or {}
    lang = user_data.get("lang", "fa")
    
    await query.answer()

    # ==================== سیستم زبان ====================
    if data == "lang":
        # منوی انتخاب زبان
        keyboard = [
            [InlineKeyboardButton("🇮🇷 فارسی", callback_data="setlang_fa")],
            [InlineKeyboardButton("🇺🇸 English", callback_data="setlang_en")],
            [InlineKeyboardButton(get_text("back_previous", lang=lang), callback_data="back_prev")],
            [InlineKeyboardButton(get_text("back_to_main", lang=lang), callback_data="main_menu")]
        ]
        await query.edit_message_text(
            text=get_text("choose_language", lang=lang),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        
    elif data.startswith("setlang_"):
        # تغییر زبان
        new_lang = data.replace("setlang_", "")
        user_data["lang"] = new_lang
        upsert_user(user.id, user_data)
        
        # نمایش نام زبان
        lang_name = "فارسی" if new_lang == "fa" else "English"
        
        # مستقیماً منوی اصلی رو با زبان جدید نشون بده
        from .navigation import go_back
        await go_back(update, context)

    # ==================== منوهای اصلی کاربران ====================
    elif data == "unlock":
        await query.edit_message_text(
            text=get_text("ask_code", lang=lang)
        )
        
    elif data == "support":
        support_text = await get_support_message(user.id, lang)
        await query.edit_message_text(
            text=support_text
        )
        
    elif data == "profile":
        await profile_cmd(update, context)
        
    elif data == "my_groups":
        await list_groups_cmd(update, context)
        
    elif data == "scheduler":
        await scheduler_menu(update, context)
        
    elif data == "send_now":
        await send_now_menu(update, context)

    # ==================== منوهای مدیریتی ادمین ====================
    elif data == "admin_users_management":
        if not is_admin(user.id):
            await query.edit_message_text(text="Access denied.")
            return
        text = "👤 مدیریت کاربران - گزینه مورد نظر را انتخاب کنید:" if lang == "fa" else "👤 User Management - Choose an option:"
        keyboard = [
            [InlineKeyboardButton("📋 لیست کاربران", callback_data="admin_list_users")],
            [InlineKeyboardButton("🔍 جستجوی کاربر", callback_data="admin_search_user")],
            [InlineKeyboardButton("⬆️ ارتقا به ادمین", callback_data="admin_promote_user")],
            [InlineKeyboardButton("🔒 قفل کاربر", callback_data="admin_lock_user")],
            [InlineKeyboardButton("🔓 آزاد کردن کاربر", callback_data="admin_unlock_user")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_admin_main")]
        ]
        if lang != "fa":
            keyboard = [
                [InlineKeyboardButton("📋 List Users", callback_data="admin_list_users")],
                [InlineKeyboardButton("🔍 Search User", callback_data="admin_search_user")],
                [InlineKeyboardButton("⬆️ Promote to Admin", callback_data="admin_promote_user")],
                [InlineKeyboardButton("🔒 Lock User", callback_data="admin_lock_user")],
                [InlineKeyboardButton("🔓 Unlock User", callback_data="admin_unlock_user")],
                [InlineKeyboardButton("🔙 Back", callback_data="back_to_admin_main")]
            ]
        await query.edit_message_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == "admin_groups_management":
        if not is_admin(user.id):
            await query.edit_message_text(text="Access denied.")
            return
        text = "👥 مدیریت گروه‌ها - گزینه مورد نظر را انتخاب کنید:" if lang == "fa" else "👥 Groups Management - Choose an option:"
        keyboard = [
            [InlineKeyboardButton("📋 لیست گروه‌های من", callback_data="user_groups_menu")],
            [InlineKeyboardButton("➕ اضافه کردن گروه", callback_data="admin_add_group")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_admin_main")]
        ]
        if lang != "fa":
            keyboard = [
                [InlineKeyboardButton("📋 My Groups List", callback_data="user_groups_menu")],
                [InlineKeyboardButton("➕ Add Group", callback_data="admin_add_group")],
                [InlineKeyboardButton("🔙 Back", callback_data="back_to_admin_main")]
            ]
        await query.edit_message_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == "admin_codes_management":
        if not is_admin(user.id):
            await query.edit_message_text(text="Access denied.")
            return
        text = "🔑 مدیریت کدها - گزینه مورد نظر را انتخاب کنید:" if lang == "fa" else "🔑 Codes Management - Choose an option:"
        keyboard = [
            [InlineKeyboardButton("🧪 کد تست یک روزه", callback_data="admin_test_code")],
            [InlineKeyboardButton("📅 کد ۱ ماهه", callback_data="admin_1month_code")],
            [InlineKeyboardButton("📅 کد ۳ ماهه", callback_data="admin_3month_code")],
            [InlineKeyboardButton("📅 کد ۴ ماهه", callback_data="admin_4month_code")],
            [InlineKeyboardButton("🎁 کد هدیه", callback_data="admin_gift_code")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_admin_main")]
        ]
        if lang != "fa":
            keyboard = [
                [InlineKeyboardButton("🧪 1-Day Test Code", callback_data="admin_test_code")],
                [InlineKeyboardButton("📅 1-Month Code", callback_data="admin_1month_code")],
                [InlineKeyboardButton("📅 3-Month Code", callback_data="admin_3month_code")],
                [InlineKeyboardButton("📅 4-Month Code", callback_data="admin_4month_code")],
                [InlineKeyboardButton("🎁 Gift Code", callback_data="admin_gift_code")],
                [InlineKeyboardButton("🔙 Back", callback_data="back_to_admin_main")]
            ]
        await query.edit_message_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == "admin_admins_management":
        if not is_admin(user.id):
            await query.edit_message_text(text="Access denied.")
            return
        text = "⚙️ مدیریت ادمین‌ها - گزینه مورد نظر را انتخاب کنید:" if lang == "fa" else "⚙️ Admins Management - Choose an option:"
        keyboard = [
            [InlineKeyboardButton("📋 لیست ادمین‌ها", callback_data="admin_list_admins")],
            [InlineKeyboardButton("➕ اضافه کردن ادمین", callback_data="admin_add_admin")],
            [InlineKeyboardButton("🗑 حذف ادمین", callback_data="admin_remove_admin")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_admin_main")]
        ]
        if lang != "fa":
            keyboard = [
                [InlineKeyboardButton("📋 List Admins", callback_data="admin_list_admins")],
                [InlineKeyboardButton("➕ Add Admin", callback_data="admin_add_admin")],
                [InlineKeyboardButton("🗑 Remove Admin", callback_data="admin_remove_admin")],
                [InlineKeyboardButton("🔙 Back", callback_data="back_to_admin_main")]
            ]
        await query.edit_message_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == "admin_messages_management":
        if not is_admin(user.id):
            await query.edit_message_text(text="Access denied.")
            return
        text = "📨 مدیریت پیام‌ها - گزینه مورد نظر را انتخاب کنید:" if lang == "fa" else "📨 Messages Management - Choose an option:"
        keyboard = [
            [InlineKeyboardButton("📨 ارسال به همه", callback_data="admin_broadcast")],
            [InlineKeyboardButton("📤 ارسال به کاربر", callback_data="admin_send_user")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_admin_main")]
        ]
        if lang != "fa":
            keyboard = [
                [InlineKeyboardButton("📨 Broadcast to All", callback_data="admin_broadcast")],
                [InlineKeyboardButton("📤 Send to User", callback_data="admin_send_user")],
                [InlineKeyboardButton("🔙 Back", callback_data="back_to_admin_main")]
            ]
        await query.edit_message_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # ==================== منوهای کاربران آزاد ====================
    elif data == "user_messages_management":
        if user_data.get("locked", True):
            await query.edit_message_text(text="Account is locked." if lang != "fa" else "حساب قفل است.")
            return
        text = "📨 مدیریت پیام‌ها - گزینه مورد نظر را انتخاب کنید:" if lang == "fa" else "📨 Messages Management - Choose an option:"
        keyboard = [
            [InlineKeyboardButton("⏰ زمان‌بندی پیام", callback_data="user_scheduler_menu")],
            [InlineKeyboardButton("🚀 ارسال فوری", callback_data="user_send_now_menu")],
            [InlineKeyboardButton("📨 پیام به ادمین", callback_data="user_message_admin")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_user_main")]
        ]
        if lang != "fa":
            keyboard = [
                [InlineKeyboardButton("⏰ Schedule Message", callback_data="user_scheduler_menu")],
                [InlineKeyboardButton("🚀 Instant Send", callback_data="user_send_now_menu")],
                [InlineKeyboardButton("📨 Message to Admin", callback_data="user_message_admin")],
                [InlineKeyboardButton("🔙 Back", callback_data="back_to_user_main")]
            ]
        await query.edit_message_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == "user_groups_management":
        if user_data.get("locked", True):
            await query.edit_message_text(text="Account is locked." if lang != "fa" else "حساب قفل است.")
            return
        await groups_menu(update, context)

    # ==================== اجرای عملیات ادمین ====================
    elif data == "admin_list_users":
        if not is_admin(user.id):
            await query.edit_message_text(text="Access denied.")
            return
        await admin_list_users(update, context)

    elif data == "admin_search_user":
        if not is_admin(user.id):
            await query.edit_message_text(text="Access denied.")
            return
        text = "🔍 لطفاً آیدی کاربر را وارد کنید:" if lang == "fa" else "🔍 Please enter user ID:"
        await query.edit_message_text(text=text)
        # ذخیره state برای دریافت آیدی کاربر
        context.user_data["waiting_for_user_id"] = True

    elif data == "admin_promote_user":
        if not is_admin(user.id):
            await query.edit_message_text(text="Access denied.")
            return
        text = "⬆️ لطفاً آیدی کاربر را برای ارتقا وارد کنید:" if lang == "fa" else "⬆️ Please enter user ID to promote:"
        await query.edit_message_text(text=text)
        context.user_data["waiting_for_promote_user"] = True

    elif data == "admin_lock_user":
        if not is_admin(user.id):
            await query.edit_message_text(text="Access denied.")
            return
        text = "🔒 لطفاً آیدی کاربر را برای قفل کردن وارد کنید:" if lang == "fa" else "🔒 Please enter user ID to lock:"
        await query.edit_message_text(text=text)
        context.user_data["waiting_for_lock_user"] = True

    elif data == "admin_unlock_user":
        if not is_admin(user.id):
            await query.edit_message_text(text="Access denied.")
            return
        text = "🔓 لطفاً آیدی کاربر را برای آزاد کردن وارد کنید:" if lang == "fa" else "🔓 Please enter user ID to unlock:"
        await query.edit_message_text(text=text)
        context.user_data["waiting_for_unlock_user"] = True

    elif data == "admin_test_code":
        if not is_admin(user.id):
            await query.edit_message_text(text="Access denied.")
            return
        await admin_generate_test_code(update, context)

    elif data == "admin_1month_code":
        if not is_admin(user.id):
            await query.edit_message_text(text="Access denied.")
            return
        await admin_generate_1month_code(update, context)

    elif data == "admin_3month_code":
        if not is_admin(user.id):
            await query.edit_message_text(text="Access denied.")
            return
        await admin_generate_3month_code(update, context)

    elif data == "admin_4month_code":
        if not is_admin(user.id):
            await query.edit_message_text(text="Access denied.")
            return
        await admin_generate_4month_code(update, context)

    elif data == "admin_gift_code":
        if not is_admin(user.id):
            await query.edit_message_text(text="Access denied.")
            return
        text = "🎁 لطفاً تعداد استفاده کد هدیه را وارد کنید:" if lang == "fa" else "🎁 Please enter gift code max uses:"
        await query.edit_message_text(text=text)
        context.user_data["waiting_for_gift_uses"] = True

    elif data == "admin_list_admins":
        if not is_admin(user.id):
            await query.edit_message_text(text="Access denied.")
            return
        await admin_list_admins(update, context)

    elif data == "admin_add_admin":
        if not is_admin(user.id):
            await query.edit_message_text(text="Access denied.")
            return
        text = "➕ لطفاً آیدی کاربر را برای اضافه کردن به ادمین وارد کنید:" if lang == "fa" else "➕ Please enter user ID to add as admin:"
        await query.edit_message_text(text=text)
        context.user_data["waiting_for_add_admin"] = True

    elif data == "admin_remove_admin":
        if not is_admin(user.id):
            await query.edit_message_text(text="Access denied.")
            return
        text = "🗑 لطفاً آیدی ادمین را برای حذف وارد کنید:" if lang == "fa" else "🗑 Please enter admin ID to remove:"
        await query.edit_message_text(text=text)
        context.user_data["waiting_for_remove_admin"] = True

    elif data == "admin_broadcast":
        if not is_admin(user.id):
            await query.edit_message_text(text="Access denied.")
            return
        text = "📨 لطفاً پیام خود را برای ارسال به همه کاربران وارد کنید:" if lang == "fa" else "📨 Please enter message to broadcast:"
        await query.edit_message_text(text=text)
        context.user_data["waiting_for_broadcast"] = True

    elif data == "admin_send_user":
        if not is_admin(user.id):
            await query.edit_message_text(text="Access denied.")
            return
        text = "📤 لطفاً آیدی کاربر و پیام را وارد کنید (با فاصله):" if lang == "fa" else "📤 Please enter user ID and message (separated by space):"
        await query.edit_message_text(text=text)
        context.user_data["waiting_for_send_user"] = True

    # ==================== اجرای عملیات کاربران ====================
    elif data == "user_scheduler_menu":
        if user_data.get("locked", True):
            await query.edit_message_text(text="Account is locked." if lang != "fa" else "حساب قفل است.")
            return
        await scheduler_menu(update, context)

    elif data == "user_send_now_menu":
        if user_data.get("locked", True):
            await query.edit_message_text(text="Account is locked." if lang != "fa" else "حساب قفل است.")
            return
        await send_now_menu(update, context)

    elif data == "user_message_admin":
        if user_data.get("locked", True):
            await query.edit_message_text(text="Account is locked." if lang != "fa" else "حساب قفل است.")
            return
        text = "📨 لطفاً پیام خود را برای ادمین وارد کنید:" if lang == "fa" else "📨 Please enter your message for admin:"
        await query.edit_message_text(text=text)
        context.user_data["waiting_for_admin_message"] = True

    elif data == "admin_add_group":
        if not is_admin(user.id):
            await query.edit_message_text(text="Access denied.")
            return
        text = "➕ لطفاً آیدی گروه را برای اضافه کردن وارد کنید:" if lang == "fa" else "➕ Please enter group ID to add:"
        await query.edit_message_text(text=text)
        context.user_data["waiting_for_add_group"] = True

    # ==================== ناوبری و بازگشت ====================
    elif data == "back_to_admin_main":
        if not is_admin(user.id):
            await query.edit_message_text(text="Access denied.")
            return
        text = "👑 پنل مدیریت - بخش مورد نظر را انتخاب کنید:" if lang == "fa" else "👑 Admin Panel - Choose management section:"
        await query.edit_message_text(
            text=text,
            reply_markup=admin_main_menu(lang)
        )

    elif data == "back_to_user_main":
        if user_data.get("locked", True):
            text = get_text("start_locked", lang=lang)
            await query.edit_message_text(
                text=text,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(get_text("menu_language", lang=lang), callback_data="lang")],
                    [InlineKeyboardButton(get_text("menu_unlock", lang=lang), callback_data="unlock")],
                    [InlineKeyboardButton(get_text("menu_support", lang=lang), callback_data="support")],
                ])
            )
        else:
            text = get_text("start_unlocked", lang=lang)
            await query.edit_message_text(
                text=text,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(get_text("menu_language", lang=lang), callback_data="lang")],
                    [InlineKeyboardButton(get_text("menu_my_groups", lang=lang), callback_data="my_groups")],
                    [InlineKeyboardButton(get_text("menu_scheduler", lang=lang), callback_data="scheduler")],
                    [InlineKeyboardButton(get_text("menu_send_now", lang=lang), callback_data="send_now")],
                    [InlineKeyboardButton(get_text("menu_profile", lang=lang), callback_data="profile")],
                    [InlineKeyboardButton(get_text("back_to_main", lang=lang), callback_data="main_menu")],
                ])
            )
        
    elif data in ["back_prev", "main_menu"]:
        from .navigation import go_back
        await go_back(update, context)
        
    else:
        await query.edit_message_text(
            text=get_text("unknown_action", lang=lang) or "❌ عمل ناشناخته"
)
