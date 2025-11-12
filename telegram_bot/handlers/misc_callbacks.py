# telegram_bot/handlers/misc_callbacks.py

from telegram import Update
from telegram.ext import ContextTypes
from config.messages import get_text

async def callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.callback_query.data
    user = update.effective_user
    lang = None
    await update.callback_query.answer()
    if data == "lang":
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Choose language: /setlang fa|en")
    elif data == "unlock":
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Use /unlock <CODE>")
    elif data == "support":
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Send your message and we'll forward to admins.")
    elif data == "profile":
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Use /profile")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Unknown action.")
