# telegram_bot/handlers/admin_panel.py

from telegram import Update
from telegram.ext import ContextTypes
from utils.database import is_admin, list_users
import logging

LOG = logging.getLogger(__name__)

async def admin_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if not is_admin(uid):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Access denied.")
        return
    users = list_users()
    text = f"Admin Panel\nUsers: {len(users)}\nUse other admin commands."
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
