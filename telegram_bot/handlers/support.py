# telegram_bot/handlers/support.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler, MessageHandler, filters, ConversationHandler
from utils.tg_helpers import safe_send_message
from utils.database import get_admins, get_user
from keyboards.support_keyboards import (
    get_admins_list_keyboard,
    get_admin_management_keyboard,
    get_support_success_keyboard,
    get_support_cancel_keyboard
)
import logging

LOG = logging.getLogger(__name__)

# حالت‌های مکالمه
SELECTING_ADMIN, WRITING_MESSAGE = range(2)

async def support_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """شروع فرآیند پشتیبانی - نمایش لیست ادمین‌ها"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user_data = get_user(user_id) or {}
    lang = user_data.get("lang", "fa")
    
    admins = get_admins()
    
    # فقط ادمین‌های visible رو نمایش بده
    visible_admins = [admin for admin in admins if admin.get('visible', True)]
    
    if not visible_admins:
        text = (
            "📞 در حال حاضر ادمینی برای پشتیبانی موجود نیست. لطفاً بعداً تلاش کنید." 
            if lang == "fa" else 
            "📞 No admins available for support at the moment. Please try again later."
        )
        await query.edit_message_text(text)
        return
    
    text = (
        "👥 لطفاً ادمین مورد نظر را انتخاب کنید:" 
        if lang == "fa" else 
        "👥 Please select an admin:"
    )
    
    await query.edit_message_text(
        text,
        reply_markup=get_admins_list_keyboard(visible_admins, lang)
    )

async def select_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """انتخاب ادمین برای پشتیبانی"""
    query = update.callback_query
    await query.answer()
    
    admin_id = int(query.data.replace("support_admin_", ""))
    context.user_data['support_admin_id'] = admin_id
    context.user_data['support_admin_name'] = None
    
    user_id = query.from_user.id
    user_data = get_user(user_id) or {}
    lang = user_data.get("lang", "fa")
    
    # پیدا کردن نام ادمین
    admins = get_admins()
    admin_name = f"Admin {admin_id}"
    for admin in admins:
        if admin['user_id'] == admin_id:
            admin_name = admin.get('name', admin_name)
            context.user_data['support_admin_name'] = admin_name
            break
    
    text = (
        f"📩 شما در حال ارسال پیام به **{admin_name}** هستید.\n\n"
        f"لطفاً پیام خود را ارسال کنید:\n\n"
        f"⚠️ برای لغو از دستور /start استفاده کنید"
        if lang == "fa" else
        f"📩 You are sending a message to **{admin_name}**.\n\n"
        f"Please write your message:\n\n"
        f"⚠️ Use /start to cancel"
    )
    
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
    
    if not admin_id:
        error_text = "❌ خطا در ارسال پیام. لطفاً مجدداً تلاش کنید." 
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
        if lang == "fa":
            success_text = (
                f"✅ پیام شما با موفقیت به **{admin_name}** ارسال شد!\n\n"
                f"📝 پاسخ ادمین به همین چت برای شما ارسال خواهد شد."
            )
        else:
            success_text = (
                f"✅ Your message has been sent to **{admin_name}** successfully!\n\n"
                f"📝 Admin's reply will be sent to this chat."
            )
        
        await update.message.reply_text(
            success_text,
            reply_markup=get_support_success_keyboard(lang)
        )
        
    except Exception as e:
        LOG.error(f"Failed to send support message to admin {admin_id}: {e}")
        
        if lang == "fa":
            error_text = (
                f"❌ خطا در ارسال پیام به {admin_name}.\n"
                f"لطفاً بعداً تلاش کنید یا ادمین دیگری را انتخاب کنید."
            )
        else:
            error_text = (
                f"❌ Error sending message to {admin_name}.\n"
                f"Please try again later or select another admin."
            )
        
        await update.message.reply_text(error_text)
    
    # پاک کردن داده‌های موقت
    context.user_data.pop('support_admin_id', None)
    context.user_data.pop('support_admin_name', None)
    
    return ConversationHandler.END

async def cancel_support_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """لغو فرآیند پشتیبانی از طریق دکمه"""
    query = update.callback_query
    await query.answer()
    
    context.user_data.pop('support_admin_id', None)
    context.user_data.pop('support_admin_name', None)
    
    user_data = get_user(query.from_user.id) or {}
    lang = user_data.get("lang", "fa")
    
    text = "❌ ارسال پیام لغو شد." if lang == "fa" else "❌ Message sending cancelled."
    
    await query.edit_message_text(text)

async def cancel_support_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """لغو فرآیند پشتیبانی از طریق دستور"""
    context.user_data.pop('support_admin_id', None)
    context.user_data.pop('support_admin_name', None)
    
    user_data = get_user(update.effective_user.id) or {}
    lang = user_data.get("lang", "fa")
    
    text = "❌ ارسال پیام لغو شد." if lang == "fa" else "❌ Message sending cancelled."
    await update.message.reply_text(text)
    
    return ConversationHandler.END

# هندلر پاسخ ادمین به کاربر (برای پیاده‌سازی بعدی)
async def handle_admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """مدیریت پاسخ ادمین به کاربر"""
    query = update.callback_query
    await query.answer()
    
    # این قسمت رو بعداً کامل می‌کنیم
    await query.message.reply_text("سیستم پاسخ‌دهی به زودی اضافه خواهد شد.")

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
    
    # هندلرهای پاسخ ادمین (موقت)
    app.add_handler(CallbackQueryHandler(handle_admin_reply, pattern="^reply_to_"))
    app.add_handler(CallbackQueryHandler(handle_admin_reply, pattern="^support_done_"))
    app.add_handler(CallbackQueryHandler(handle_admin_reply, pattern="^block_user_"))

# تابع قدیمی برای سازگاری
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
admin_list = "\n".join(admin_list)
            def get_support_message() -> str:
    # کدهای قبلی...
    
    if admin_list:
        text = f"📞 Support\n\nContact the following admins for help:\n{admin_list}"
    else:
        text = "📞 Support\n\nNo admins available at the moment. Please try again later."
    
    return text

# تابع قدیمی برای سازگاری
async def text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """تابع قدیمی - غیرفعال شده"""
    user = update.effective_user
    user_data = get_user(user.id) or {}
    lang = user_data.get("lang", "fa")
    
    text = (
        "⚠️ لطفاً از دکمه 📞 پشتیبانی در منوی اصلی استفاده کنید." 
        if lang == "fa" else 
        "⚠️ Please use the 📞 Support button in the main menu."
    )
    
    await update.message.reply_text(text)
