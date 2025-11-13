# telegram_bot/handlers/admin_admins_handlers.py
from telegram import Update
from telegram.ext import ContextTypes
from utils.database import is_admin, get_admins, add_admin, remove_admin, get_user
from config.messages import get_text
import logging

LOG = logging.getLogger(__name__)

async def admin_list_admins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """لیست ادمین‌ها"""
    uid = update.effective_user.id
    if not is_admin(uid):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Access denied.")
        return
    
    user_data = get_user(uid) or {}
    lang = user_data.get("lang", "fa")
    
    admins = get_admins()
    if not admins:
        text = "📭 هیچ ادمینی وجود ندارد" if lang == "fa" else "📭 No admins found"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return
    
    text = "📋 لیست ادمین‌ها:\n\n" if lang == "fa" else "📋 Admins List:\n\n"
    for i, admin in enumerate(admins, 1):
        admin_id = admin.get("user_id", "")
        level = admin.get("level", 1)
        level_text = "سطح ۱" if level == 1 else "سطح ۲"
        if lang != "fa":
            level_text = f"Level {level}"
        
        # اطلاعات کاربر
        admin_user = get_user(admin_id) or {}
        locked = admin_user.get("locked", True)
        status = "🔓 فعال" if not locked else "🔒 قفل"
        if lang != "fa":
            status = "🔓 Active" if not locked else "🔒 Locked"
        
        text += f"{i}. ID: {admin_id} | {level_text} | {status}\n"
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

async def admin_add_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """اضافه کردن ادمین جدید"""
    uid = update.effective_user.id
    if not is_admin(uid):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Access denied.")
        return
    
    user_data = get_user(uid) or {}
    lang = user_data.get("lang", "fa")
    
    if not context.args:
        text = "➕ لطفاً آیدی کاربر و سطح را وارد کنید: /addadmin <user_id> <level>" if lang == "fa" else "➕ Please enter user ID and level: /addadmin <user_id> <level>"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return
    
    try:
        target_id = int(context.args[0])
        level = int(context.args[1]) if len(context.args) > 1 else 2
        
        add_admin(target_id, level=level)
        
        text = f"✅ کاربر {target_id} به ادمین سطح {level} اضافه شد" if lang == "fa" else f"✅ User {target_id} added as admin level {level}"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        
    except ValueError:
        text = "❌ آیدی کاربر و سطح باید عدد باشند" if lang == "fa" else "❌ User ID and level must be numbers"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

async def admin_remove_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """حذف ادمین"""
    uid = update.effective_user.id
    if not is_admin(uid):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Access denied.")
        return
    
    user_data = get_user(uid) or {}
    lang = user_data.get("lang", "fa")
    
    if not context.args:
        text = "🗑 لطفاً آیدی ادمین را وارد کنید: /removeadmin <user_id>" if lang == "fa" else "🗑 Please enter admin ID: /removeadmin <user_id>"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return
    
    try:
        target_id = int(context.args[0])
        
        remove_admin(target_id)
        
        text = f"✅ ادمین {target_id} حذف شد" if lang == "fa" else f"✅ Admin {target_id} removed"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        
    except ValueError:
        text = "❌ آیدی ادمین باید عدد باشد" if lang == "fa" else "❌ Admin ID must be a number"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
