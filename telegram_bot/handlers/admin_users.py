# telegram_bot/handlers/admin_users.py

from telegram import Update
from telegram.ext import ContextTypes
from utils.database import is_admin, add_admin, remove_admin

async def add_admin_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if not is_admin(uid):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Access denied.")
        return
    if not context.args:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Usage: /addadmin <user_id>")
        return
    target = int(context.args[0])
    add_admin(target, level=2)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Added admin {target}")
