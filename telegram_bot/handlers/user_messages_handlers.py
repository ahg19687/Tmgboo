# telegram_bot/handlers/user_messages_handlers.py
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from utils.database import get_user, is_admin
from utils.tg_helpers import safe_send_message
from config.messages import get_text
import logging

LOG = logging.getLogger(__name__)

async def user_schedule_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """زمان‌بندی پیام برای کاربران آزاد"""
    uid = update.effective_user.id
    user_data = get_user(uid) or {}
    lang = user_data.get("lang", "fa")
    
    if user_data.get("locked", True):
        text = "🔒 حساب شما قفل است. لطفاً اول قفل‌گشایی کنید." if lang == "fa" else "🔒 Your account is locked. Please unlock first."
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return
    
    if not context.args:
        text = "⏰ لطفاً زمان و پیام را وارد کنید: /schedule <HH:MM> <message>" if lang == "fa" else "⏰ Please enter time and message: /schedule <HH:MM> <message>"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return
    
    time_str = context.args[0]
    message = " ".join(context.args[1:])
    
    # اینجا باید با سیستم زمان‌بندی موجود یکپارچه شود
    from .message_scheduler import schedule_cmd
    await schedule_cmd(update, context)

async def user_instant_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ارسال فوری پیام برای کاربران آزاد"""
    uid = update.effective_user.id
    user_data = get_user(uid) or {}
    lang = user_data.get("lang", "fa")
    
    if user_data.get("locked", True):
        text = "🔒 حساب شما قفل است. لطفاً اول قفل‌گشایی کنید." if lang == "fa" else "🔒 Your account is locked. Please unlock first."
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return
    
    if not context.args:
        text = "🚀 لطفاً پیام خود را وارد کنید: /send <message>" if lang == "fa" else "🚀 Please enter your message: /send <message>"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return
    
    message = " ".join(context.args)
    groups = user_data.get("groups", [])
    
    if not groups:
        text = "❌ هیچ گروهی ثبت نشده است. لطفاً اول گروه اضافه کنید." if lang == "fa" else "❌ No groups registered. Please add a group first."
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return
    
    success_count = 0
    for group_id in groups:
        try:
            await safe_send_message(context.bot, group_id, message)
            success_count += 1
        except Exception as e:
            LOG.warning(f"Failed to send message to group {group_id}: {e}")
    
    if lang == "fa":
        text = f"✅ پیام با موفقیت به {success_count} از {len(groups)} گروه ارسال شد"
    else:
        text = f"✅ Message successfully sent to {success_count} out of {len(groups)} groups"
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

async def user_message_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ارسال پیام به ادمین برای کاربران آزاد"""
    uid = update.effective_user.id
    user_data = get_user(uid) or {}
    lang = user_data.get("lang", "fa")
    
    if not context.args:
        text = "📨 لطفاً پیام خود را وارد کنید: /toadmin <message>" if lang == "fa" else "📨 Please enter your message: /toadmin <message>"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return
    
    message = " ".join(context.args)
    
    # استفاده از سیستم پشتیبانی موجود
    from .support import text_message
    await text_message(update, context)
