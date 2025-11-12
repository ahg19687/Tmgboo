# telegram_bot/handlers/support.py

from telegram import Update
from telegram.ext import ContextTypes
from utils.tg_helpers import safe_send_message
from utils.database import get_admins
import logging

LOG = logging.getLogger(__name__)

async def text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # receives any free text from user -> forward to admins
    user = update.effective_user
    text = update.message.text
    admins = get_admins()
    meta = f"Support message from user {user.id}"
    # forward text to admins (no local storage of content)
    for a in admins:
        try:
            await safe_send_message(context.bot, a["user_id"], f"{meta}\n\n{text}")
        except Exception as e:
            LOG.warning("failed to forward support msg to %s: %s", a["user_id"], str(e))
