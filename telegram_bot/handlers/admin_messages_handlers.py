# telegram_bot/handlers/admin_messages_handlers.py
from telegram import Update
from telegram.ext import ContextTypes
from utils.database import is_admin, get_user, list_users
from utils.tg_helpers import safe_send_message
from config.messages import get_text
import logging

LOG = logging.getLogger(__name__)

async def admin_broadcast_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ارسال پیام به همه کاربران"""
    uid = update.effective_user.id
    if not is_admin(uid):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Access denied.")
        return
    
    user_data = get_user(uid) or {}
    lang = user_data.get("lang", "fa")
    
    if not context.args:
        text = "📨 لطفاً پیام خود را وارد کنید: /broadcast <message>" if lang == "fa" else "📨 Please enter your message: /broadcast <message>"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return
    
    message = " ".join(context.args)
    users = list_users()
    
    if lang == "fa":
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"📨 در حال ارسال پیام به {len(users)} کاربر...")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"📨 Sending message to {len(users)} users...")
    
    success_count = 0
    for user in users:
        try:
            await safe_send_message(context.bot, user["user_id"], message)
            success_count += 1
        except Exception as e:
            LOG.warning(f"Failed to send broadcast to {user['user_id']}: {e}")
    
    if lang == "fa":
        text = f"✅ پیام با موفقیت به {success_count} از {len(users)} کاربر ارسال شد"
    else:
        text = f"✅ Message successfully sent to {success_count} out of {len(users)} users"
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

async def admin_send_to_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ارسال پیام به کاربر خاص"""
    uid = update.effective_user.id
    if not is_admin(uid):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Access denied.")
        return
    
    user_data = get_user(uid) or {}
    lang = user_data.get("lang", "fa")
    
    if len(context.args) < 2:
        text = "📤 لطفاً آیدی کاربر و پیام را وارد کنید: /senduser <user_id> <message>" if lang == "fa" else "📤 Please enter user ID and message: /senduser <user_id> <message>"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return
    
    try:
        target_id = int(context.args[0])
        message = " ".join(context.args[1:])
        
        await safe_send_message(context.bot, target_id, message)
        
        text = f"✅ پیام به کاربر {target_id} ارسال شد" if lang == "fa" else f"✅ Message sent to user {target_id}"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        
    except ValueError:
        text = "❌ آیدی کاربر باید عدد باشد" if lang == "fa" else "❌ User ID must be a number"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    except Exception as e:
        text = f"❌ خطا در ارسال پیام: {e}" if lang == "fa" else f"❌ Error sending message: {e}"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
