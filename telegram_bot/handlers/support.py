# telegram_bot/handlers/support.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler, MessageHandler, filters, ConversationHandler
from utils.tg_helpers import safe_send_message
from utils.database import get_admins, get_user, upsert_user
from keyboards.support_keyboards import (
    get_admins_list_keyboard,
    get_admin_management_keyboard,
    get_support_success_keyboard,
    get_support_cancel_keyboard,
    get_user_reply_keyboard
)
from config.messages import get_text
import logging

LOG = logging.getLogger(__name__)

# حالت‌های مکالمه
SELECTING_ADMIN, WRITING_MESSAGE = range(2)

# دیکشنری برای مدیریت وضعیت پشتیبانی
support_sessions = {}
admin_reply_sessions = {}
user_reply_sessions = {}

def is_user_in_support_mode(user_id):
    return support_sessions.get(user_id, False)

def set_support_mode(user_id, admin_id=None):
    support_sessions[user_id] = {"admin_id": admin_id, "active": True}

def clear_support_mode(user_id):
    if user_id in support_sessions:
        del support_sessions[user_id]

def is_admin_in_reply_mode(admin_id, user_id=None):
    if admin_id in admin_reply_sessions:
        if user_id:
            return admin_reply_sessions[admin_id].get("target_user_id") == user_id
        return True
    return False

def set_admin_reply_mode(admin_id, target_user_id):
    admin_reply_sessions[admin_id] = {"target_user_id": target_user_id, "active": True}

def clear_admin_reply_mode(admin_id):
    if admin_id in admin_reply_sessions:
        del admin_reply_sessions[admin_id]

def is_user_in_reply_mode(user_id, admin_id=None):
    if user_id in user_reply_sessions:
        if admin_id:
            return user_reply_sessions[user_id].get("admin_id") == admin_id
        return True
    return False

def set_user_reply_mode(user_id, admin_id):
    user_reply_sessions[user_id] = {"admin_id": admin_id, "active": True}

def clear_user_reply_mode(user_id):
    if user_id in user_reply_sessions:
        del user_reply_sessions[user_id]

async def support_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """شروع فرآیند پشتیبانی - نمایش لیست ادمین‌ها"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user_data = get_user(user_id) or {}
    lang = user_data.get("lang", "fa")
    
    admins = get_admins()
    visible_admins = [admin for admin in admins if admin.get('visible', True)]
    
    if not visible_admins:
        text = get_text("no_admins_available", lang=lang)
        await query.edit_message_text(text)
        return
    
    text = get_text("select_admin_for_support", lang=lang)
    
    await query.edit_message_text(
        text,
        reply_markup=get_admins_list_keyboard(visible_admins, lang)
    )

async def select_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """انتخاب ادمین برای پشتیبانی"""
    query = update.callback_query
    await query.answer()
    
    admin_id = int(query.data.replace("support_admin_", ""))
    user_id = query.from_user.id
    
    # تنظیم حالت پشتیبانی برای کاربر
    set_support_mode(user_id, admin_id)
    
    user_data = get_user(user_id) or {}
    lang = user_data.get("lang", "fa")
    
    # پیدا کردن نام ادمین
    admins = get_admins()
    admin_name = f"Admin {admin_id}"
    for admin in admins:
        if admin['user_id'] == admin_id:
            admin_name = admin.get('name', admin_name)
            break
    
    context.user_data['support_admin_id'] = admin_id
    context.user_data['support_admin_name'] = admin_name
    
    text = get_text("write_support_message", lang=lang).format(admin_name=admin_name)
    
    await query.edit_message_text(
        text,
        reply_markup=get_support_cancel_keyboard(lang)
    )
    return WRITING_MESSAGE

async def handle_support_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دریافت و ارسال پیام پشتیبانی به ادمین انتخابی"""
    user_id = update.message.from_user.id
    admin_id = context.user_data.get('support_admin_id')
    user_message = update.message.text
    
    if not admin_id or not is_user_in_support_mode(user_id):
        error_text = get_text("support_send_error", lang="fa")
        await update.message.reply_text(error_text)
        return ConversationHandler.END
    
    user_data = get_user(user_id) or {}
    lang = user_data.get("lang", "fa")
    
    user_name = user_data.get('name', f'User {user_id}')
    admin_name = context.user_data.get('support_admin_name', f'Admin {admin_id}')
    
    try:
        # ارسال پیام به ادمین انتخابی
        if lang == "fa":
            admin_message = (
                f"📩 **پیام پشتیبانی از کاربر**\n\n"
                f"👤 **کاربر:** {user_name}\n"
                f"🆔 **آیدی:** `{user_id}`\n"
                f"📝 **پیام:**\n{user_message}"
            )
        else:
            admin_message = (
                f"📩 **Support Message from User**\n\n"
                f"👤 **User:** {user_name}\n"
                f"🆔 **ID:** `{user_id}`\n"
                f"📝 **Message:**\n{user_message}"
            )
        
        await safe_send_message(
            context.bot, 
            admin_id, 
            admin_message,
            reply_markup=get_admin_management_keyboard(user_id, lang)
        )
        
        # تأیید به کاربر
        success_text = get_text("support_message_sent", lang=lang).format(admin_name=admin_name)
        
        await update.message.reply_text(
            success_text,
            reply_markup=get_support_success_keyboard(lang)
        )
        
    except Exception as e:
        LOG.error(f"Failed to send support message to admin {admin_id}: {e}")
        error_text = get_text("support_send_failed", lang=lang).format(admin_name=admin_name)
        await update.message.reply_text(error_text)
    
    # غیرفعال کردن سیستم پشتیبانی
    clear_support_mode(user_id)
    context.user_data.pop('support_admin_id', None)
    context.user_data.pop('support_admin_name', None)
    
    return ConversationHandler.END

async def handle_message_seen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """مدیریت دکمه 'سین' ادمین"""
    query = update.callback_query
    await query.answer()
    
    user_id = int(query.data.replace("support_done_", ""))
    admin_id = query.from_user.id
    
    user_data = get_user(user_id) or {}
    lang = user_data.get("lang", "fa")
    admin_data = get_user(admin_id) or {}
    admin_name = admin_data.get('name', f'Admin {admin_id}')
    
    # اطلاع به کاربر
    seen_text = get_text("admin_seen_message", lang=lang).format(admin_name=admin_name)
    await safe_send_message(context.bot, user_id, seen_text)
    
    # اطلاع به ادمین
    await query.message.reply_text(get_text("marked_as_seen", lang="fa"))
    
    # غیرفعال کردن حالت
    clear_support_mode(user_id)

async def handle_admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """شروع فرآیند پاسخ ادمین"""
    query = update.callback_query
    await query.answer()
    
    user_id = int(query.data.replace("reply_to_", ""))
    admin_id = query.from_user.id
    
    # تنظیم حالت پاسخ ادمین
    set_admin_reply_mode(admin_id, user_id)
    
    admin_data = get_user(admin_id) or {}
    lang = admin_data.get("lang", "fa")
    
    user_data = get_user(user_id) or {}
    user_name = user_data.get('name', f'User {user_id}')
    
    text = get_text("write_reply_to_user", lang=lang).format(user_name=user_name)
    
    await query.message.reply_text(text)
    
    # ذخیره اطلاعات برای استفاده در هندلر پیام
    context.user_data['reply_target_user_id'] = user_id
    context.user_data['reply_target_user_name'] = user_name

async def handle_admin_reply_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پردازش پیام پاسخ ادمین"""
    admin_id = update.message.from_user.id
    user_id = context.user_data.get('reply_target_user_id')
    reply_message = update.message.text
    
    if not user_id or not is_admin_in_reply_mode(admin_id, user_id):
        error_text = get_text("reply_mode_inactive", lang="fa")
        await update.message.reply_text(error_text)
        return
    
    admin_data = get_user(admin_id) or {}
    lang = admin_data.get("lang", "fa")
    admin_name = admin_data.get('name', f'Admin {admin_id}')
    
    user_data = get_user(user_id) or {}
    user_lang = user_data.get("lang", "fa")
    
    try:
        # ارسال پاسخ به کاربر
        if user_lang == "fa":
            user_reply_message = (
                f"📨 **پاسخ از پشتیبانی**\n\n"
                f"👤 **ادمین:** {admin_name}\n"
                f"📝 **پیام:**\n{reply_message}"
            )
        else:
            user_reply_message = (
                f"📨 **Reply from Support**\n\n"
                f"👤 **Admin:** {admin_name}\n"
                f"📝 **Message:**\n{reply_message}"
            )
        
        await safe_send_message(
            context.bot, 
            user_id, 
            user_reply_message,
            reply_markup=get_user_reply_keyboard(admin_id, user_lang)
        )
        
        # تأیید به ادمین
        success_text = get_text("reply_sent_to_user", lang=lang)
        await update.message.reply_text(success_text)
        
    except Exception as e:
        LOG.error(f"Failed to send reply to user {user_id}: {e}")
        error_text = get_text("reply_send_failed", lang=lang)
        await update.message.reply_text(error_text)
    
    # غیرفعال کردن حالت پاسخ
    clear_admin_reply_mode(admin_id)
    context.user_data.pop('reply_target_user_id', None)
    context.user_data.pop('reply_target_user_name', None)

async def handle_user_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """شروع فرآیند پاسخ کاربر به ادمین"""
    query = update.callback_query
    await query.answer()
    
    admin_id = int(query.data.replace("reply_to_admin_", ""))
    user_id = query.from_user.id
    
    # تنظیم حالت پاسخ کاربر
    set_user_reply_mode(user_id, admin_id)
    
    user_data = get_user(user_id) or {}
    lang = user_data.get("lang", "fa")
    
    admin_data = get_user(admin_id) or {}
    admin_name = admin_data.get('name', f'Admin {admin_id}')
    
    text = get_text("write_reply_to_admin", lang=lang).format(admin_name=admin_name)
    
    await query.message.reply_text(text)
    
    # ذخیره اطلاعات برای استفاده در هندلر پیام
    context.user_data['reply_target_admin_id'] = admin_id
    context.user_data['reply_target_admin_name'] = admin_name

async def handle_user_reply_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پردازش پیام پاسخ کاربر"""
    user_id = update.message.from_user.id
    admin_id = context.user_data.get('reply_target_admin_id')
    reply_message = update.message.text
    
    if not admin_id or not is_user_in_reply_mode(user_id, admin_id):
        error_text = get_text("reply_mode_inactive", lang="fa")
        await update.message.reply_text(error_text)
        return
    
    user_data = get_user(user_id) or {}
    lang = user_data.get("lang", "fa")
    user_name = user_data.get('name', f'User {user_id}')
    
    admin_data = get_user(admin_id) or {}
    admin_lang = admin_data.get("lang", "fa")
    
    try:
        # ارسال پاسخ به ادمین
        if admin_lang == "fa":
            admin_reply_message = (
                f"📨 **پاسخ از کاربر**\n\n"
                f"👤 **کاربر:** {user_name}\n"
                f"🆔 **آیدی:** `{user_id}`\n"
                f"📝 **پیام:**\n{reply_message}"
            )
        else:
            admin_reply_message = (
                f"📨 **Reply from User**\n\n"
                f"👤 **User:** {user_name}\n"
                f"🆔 **ID:** `{user_id}`\n"
                f"📝 **Message:**\n{reply_message}"
            )
        
        await safe_send_message(
            context.bot, 
            admin_id, 
            admin_reply_message,
            reply_markup=get_admin_management_keyboard(user_id, admin_lang)
        )
        
        # تأیید به کاربر
        success_text = get_text("reply_sent_to_admin", lang=lang)
        await update.message.reply_text(success_text)
        
    except Exception as e:
        LOG.error(f"Failed to send reply to admin {admin_id}: {e}")
        error_text = get_text("reply_send_failed", lang=lang)
        await update.message.reply_text(error_text)
    
    # غیرفعال کردن حالت پاسخ
    clear_user_reply_mode(user_id)
    context.user_data.pop('reply_target_admin_id', None)
    context.user_data.pop('reply_target_admin_name', None)

async def handle_user_seen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """مدیریت دکمه 'سین' کاربر"""
    query = update.callback_query
    await query.answer()
    
    admin_id = int(query.data.replace("seen_from_user_", ""))
    user_id = query.from_user.id
    
    user_data = get_user(user_id) or {}
    lang = user_data.get("lang", "fa")
    user_name = user_data.get('name', f'User {user_id}')
    
    admin_data = get_user(admin_id) or {}
    admin_lang = admin_data.get("lang", "fa")
    
    # اطلاع به ادمین
    seen_text = get_text("user_seen_message", lang=admin_lang).format(user_name=user_name)
    await safe_send_message(context.bot, admin_id, seen_text)
    
    # اطلاع به کاربر
    await query.message.reply_text(get_text("marked_as_seen", lang=lang))
    
    # غیرفعال کردن حالت
    clear_user_reply_mode(user_id)

async def cancel_support_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """لغو فرآیند پشتیبانی از طریق دکمه"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    clear_support_mode(user_id)
    
    context.user_data.pop('support_admin_id', None)
    context.user_data.pop('support_admin_name', None)
    
    user_data = get_user(user_id) or {}
    lang = user_data.get("lang", "fa")
    
    text = get_text("support_cancelled", lang=lang)
    await query.edit_message_text(text)

async def cancel_support_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """لغو فرآیند پشتیبانی از طریق دستور"""
    user_id = update.effective_user.id
    clear_support_mode(user_id)
    clear_admin_reply_mode(user_id)
    clear_user_reply_mode(user_id)
    
    context.user_data.pop('support_admin_id', None)
    context.user_data.pop('support_admin_name', None)
    context.user_data.pop('reply_target_user_id', None)
    context.user_data.pop('reply_target_user_name', None)
    context.user_data.pop('reply_target_admin_id', None)
    context.user_data.pop('reply_target_admin_name', None)
    
    user_data = get_user(user_id) or {}
    lang = user_data.get("lang", "fa")
    
    text = get_text("support_cancelled", lang=lang)
    await update.message.reply_text(text)
    
    return ConversationHandler.END

async def handle_regular_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """مدیریت پیام‌های عادی کاربران"""
    user_id = update.effective_user.id
    user_data = get_user(user_id) or {}
    lang = user_data.get("lang", "fa")
    
    # اگر کاربر در حالت پشتیبانی هست
    if is_user_in_support_mode(user_id):
        await handle_support_message(update, context)
        return
    
    # اگر کاربر در حالت پاسخ به ادمین هست
    if is_user_in_reply_mode(user_id):
        await handle_user_reply_message(update, context)
        return
    
    # اگر ادمین در حالت پاسخ به کاربر هست
    if is_admin_in_reply_mode(user_id):
        await handle_admin_reply_message(update, context)
        return
    
    # اگر هیچکدام نبود، پیام رو نادیده بگیر یا برای عملکردهای دیگه استفاده کن
    # اینجا می‌تونی پیام رو برای عملکردهای دیگه ربات پردازش کنی
    text = get_text("use_support_button", lang=lang)
    await update.message.reply_text(text)

# ثبت هندلرها
def register_support_handlers(app):
    # مکالمه پشتیبانی اصلی
    support_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(select_admin, pattern="^support_admin_")],
        states={
            WRITING_MESSAGE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_support_message),
                CallbackQueryHandler(cancel_support_callback, pattern="^cancel_support$")
            ]
        },
        fallbacks=[
            MessageHandler(filters.COMMAND, cancel_support_command),
            CallbackQueryHandler(cancel_support_callback, pattern="^cancel_support$")
        ],
        allow_reentry=True
    )
    
    # هندلر شروع پشتیبانی
    app.add_handler(CallbackQueryHandler(support_callback, pattern="^support$"))
    
    # هندلر مکالمه
    app.add_handler(support_conv)
    
    # هندلرهای پاسخ و سین
    app.add_handler(CallbackQueryHandler(handle_admin_reply, pattern="^reply_to_"))
    app.add_handler(CallbackQueryHandler(handle_message_seen, pattern="^support_done_"))
    app.add_handler(CallbackQueryHandler(handle_user_reply, pattern="^reply_to_admin_"))
    app.add_handler(CallbackQueryHandler(handle_user_seen, pattern="^seen_from_user_"))
    
    # هندلر پیام‌های عادی (جایگزین هندلر قدیمی)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_regular_message))

# توابع قدیمی برای سازگاری
async def get_support_message(user_id: int, lang: str = "fa"):
    """تابع قدیمی - برای سازگاری با کدهای موجود"""
    admins = get_admins()
    visible_admins = [admin for admin in admins if admin.get('visible', True)]
    
    if lang == "fa":
        if visible_admins:
            admin_list = "\n".join([f"👤 {admin.get('name', f'Admin {admin['user_id']}')}" for admin in visible_admins])
            text = f"📞 پشتیبانی\n\nبرای دریافت کمک با ادمین‌های زیر تماس بگیرید:\n{admin_list}"
        else:
            text = "📞 پشتیبانی\n\nدر حال حاضر ادمینی موجود نیست. لطفاً بعداً تلاش کنید."
    else:
        if visible_admins:
            admin_list = []
            for admin in visible_admins:
                admin_name = admin.get('name', f'Admin {admin["user_id"]}')
                admin_list.append(f"👤 {admin_name}")
            admin_list_text = "\n".join(admin_list)
            text = f"📞 Support\n\nContact the following admins for help:\n{admin_list_text}"
        else:
            text = "📞 Support\n\nNo admins available at the moment. Please try again later."
    
    return text

async def text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """تابع قدیمی - جایگزین شده با handle_regular_message"""
    await handle_regular_message(update, context)
