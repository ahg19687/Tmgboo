# telegram_bot/handlers/admin_codes.py

from telegram import Update
from telegram.ext import ContextTypes
from utils.code_tools import generate_code, create_bulk_codes, list_codes
from utils.database import is_admin
import json

async def gen_code_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if not is_admin(uid):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Access denied.")
        return
    # usage: /gencode 1m
    typ = (context.args[0] if context.args else "test")
    code = generate_code()
    # call create store
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Code: {code} ({typ})")
