# telegram_bot/handlers/message_scheduler.py

from telegram import Update
from telegram.ext import ContextTypes
from utils.scheduler import schedule_message_job
from utils.database import get_user, save_scheduled_message
from config.messages import get_text

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
