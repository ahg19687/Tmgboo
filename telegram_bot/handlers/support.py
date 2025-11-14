# telegram_bot/handlers/support.py

from telegram import Update
from telegram.ext import ContextTypes
from utils.tg_helpers import safe_send_message
from utils.database import get_admins
import logging

LOG = logging.getLogger(__name__)

async def get_support_message(user_id: int, lang: str = "fa"):
    """تابع برای نمایش پیام پشتیبانی"""
    admins = get_admins()
    
    if lang == "fa":
        if admins:
            admin_list = "\n".join([f"👤 ادمین: {admin['user_id']}" for admin in admins])
            text = f"📞 پشتیبانی\n\nبرای دریافت کد فعال‌سازی با ادمین‌های زیر تماس بگیرید:\n{admin_list}\n\nیا از دکمه 🔓 قفل‌گشایی استفاده کنید."
        else:
            text = "📞 پشتیبانی\n\nدر حال حاضر ادمینی موجود نیست. لطفاً از دکمه 🔓 قفل‌گشایی استفاده کنید."
    else:
        if admins:
            admin_list = "\n".join([f"👤 Admin: {admin['user_id']}" for admin in admins])
            text = f"📞 Support\n\nContact the following admins for unlock code:\n{admin_list}\n\nOr use the 🔓 unlock button."
        else:
            text = "📞 Support\n\nNo admins available at the moment. Please use the 🔓 unlock button."
    
    return text

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
