# telegram_bot/handlers/user_groups.py

from telegram import Update
from telegram.ext import ContextTypes
from utils.database import add_group_for_user, get_user
from config.messages import get_text

async def list_groups_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    u = get_user(uid) or {}
    groups = u.get("groups", [])
    if not groups:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=get_text("no_groups", lang=u.get("lang","fa")))
        return
    txt = "Your groups:\n" + "\n".join(str(g) for g in groups)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=txt)

# my_chat_member handler to register group when bot added
async def my_chat_member_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        chat = update.my_chat_member.chat
        if update.my_chat_member.new_chat_member.status in ("member","administrator"):
            # register group with no owner
            add_group_for_user(None, chat.id, title=chat.title or "")
    except Exception:
        pass
