# telegram_bot/handlers/message_scheduler.py
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from utils.scheduler import schedule_message_job
from utils.database import get_user, save_scheduled_message
from config.messages import get_text
from keyboards.user_keyboards import user_messages_menu

async def schedule_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    user = get_user(uid) or {}
    args = context.args
    # usage: /schedule 09:00 Your message here
    if len(args) < 2:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Usage: /schedule HH:MM message")
        return
    time_str = args[0]
    text = " ".join(args[1:])
    obj = {
        "owner_id": uid,
        "time": time_str,
        "text": text,
        "groups": user.get("groups", []),
        "enabled": True
    }
    save_scheduled_message(obj)
    schedule_message_job(obj)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Scheduled.")

async def scheduler_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """منوی زمان‌بندی پیام"""
    uid = update.effective_user.id
    user_data = get_user(uid) or {}
    lang = user_data.get("lang", "fa")
    
    if user_data.get("locked", True):
        text = "🔒 حساب شما قفل است. لطفاً اول قفل‌گشایی کنید." if lang == "fa" else "🔒 Your account is locked. Please unlock first."
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return
    
    text = "⏰ منوی زمان‌بندی پیام\n\nبرای زمان‌بندی پیام از دستور زیر استفاده کنید:\n/schedule <HH:MM> <message>\n\nمثال:\n/schedule 09:30 سلام به همه گروه‌ها" if lang == "fa" else "⏰ Message Scheduling Menu\n\nUse the following command to schedule messages:\n/schedule <HH:MM> <message>\n\nExample:\n/schedule 09:30 Hello to all groups"
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_markup=user_messages_menu(lang)
    )

async def send_now_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """منوی ارسال فوری"""
    uid = update.effective_user.id
    user_data = get_user(uid) or {}
    lang = user_data.get("lang", "fa")
    
    if user_data.get("locked", True):
        text = "🔒 حساب شما قفل است. لطفاً اول قفل‌گشایی کنید." if lang == "fa" else "🔒 Your account is locked. Please unlock first."
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return
    
    text = "🚀 منوی ارسال فوری\n\nبرای ارسال فوری پیام از دستور زیر استفاده کنید:\n/send <message>\n\nمثال:\n/send پیام تست به همه گروه‌ها" if lang == "fa" else "🚀 Instant Send Menu\n\nUse the following command to send instant messages:\n/send <message>\n\nExample:\n/send Test message to all groups"
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_markup=user_messages_menu(lang)
    )
