# telegram_bot/handlers/admin_users_handlers.py
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from utils.database import is_admin, list_users, get_user, upsert_user, add_admin, remove_admin
from utils.json_tools import load_json, save_json
from config.messages import get_text
import logging

LOG = logging.getLogger(__name__)

async def admin_list_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """لیست تمام کاربران"""
    uid = update.effective_user.id
    if not is_admin(uid):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Access denied.")
        return
    
    user_data = get_user(uid) or {}
    lang = user_data.get("lang", "fa")
    
    users = list_users()
    if not users:
        text = "📭 هیچ کاربری وجود ندارد" if lang == "fa" else "📭 No users found"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return
    
    text = "📋 لیست کاربران:\n\n" if lang == "fa" else "📋 Users List:\n\n"
    for i, user in enumerate(users[:50], 1):  # فقط 50 کاربر اول
        user_id = user.get("user_id", "")
        locked = user.get("locked", True)
        sub = user.get("subscription", {})
        status = "🔓 آزاد" if not locked else "🔒 قفل"
        if lang != "fa":
            status = "🔓 Free" if not locked else "🔒 Locked"
        
        text += f"{i}. ID: {user_id} | {status} | اشتراک: {sub.get('type', '—')}\n"
    
    if len(users) > 50:
        text += f"\n... و {len(users) - 50} کاربر دیگر" if lang == "fa" else f"\n... and {len(users) - 50} more users"
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

async def admin_search_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """جستجوی کاربر"""
    uid = update.effective_user.id
    if not is_admin(uid):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Access denied.")
        return
    
    user_data = get_user(uid) or {}
    lang = user_data.get("lang", "fa")
    
    if not context.args:
        text = "🔍 لطفاً آیدی کاربر را وارد کنید: /searchuser <user_id>" if lang == "fa" else "🔍 Please enter user ID: /searchuser <user_id>"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return
    
    try:
        target_id = int(context.args[0])
        target_user = get_user(target_id) or {}
        
        if not target_user:
            text = "❌ کاربر یافت نشد" if lang == "fa" else "❌ User not found"
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
            return
        
        # اطلاعات کاربر
        locked = target_user.get("locked", True)
        sub = target_user.get("subscription", {})
        groups = target_user.get("groups", [])
        user_lang = target_user.get("lang", "fa")
        
        if lang == "fa":
            text = f"""👤 اطلاعات کاربر:

🆔 آیدی: {target_id}
🔓 وضعیت: {'آزاد' if not locked else 'قفل'}
📅 اشتراک: {sub.get('type', '—')}
📅 انقضا: {sub.get('expires_at', '—')}
👥 گروه‌ها: {len(groups)} گروه
🌐 زبان: {'فارسی' if user_lang == 'fa' else 'انگلیسی'}"""
        else:
            text = f"""👤 User Information:

🆔 ID: {target_id}
🔓 Status: {'Free' if not locked else 'Locked'}
📅 Subscription: {sub.get('type', '—')}
📅 Expires: {sub.get('expires_at', '—')}
👥 Groups: {len(groups)} groups
🌐 Language: {'Persian' if user_lang == 'fa' else 'English'}"""
        
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        
    except ValueError:
        text = "❌ آیدی کاربر باید عدد باشد" if lang == "fa" else "❌ User ID must be a number"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

async def admin_promote_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ارتقای کاربر به ادمین"""
    uid = update.effective_user.id
    if not is_admin(uid):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Access denied.")
        return
    
    user_data = get_user(uid) or {}
    lang = user_data.get("lang", "fa")
    
    if not context.args:
        text = "⬆️ لطفاً آیدی کاربر و سطح را وارد کنید: /promote <user_id> <level>" if lang == "fa" else "⬆️ Please enter user ID and level: /promote <user_id> <level>"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return
    
    try:
        target_id = int(context.args[0])
        level = int(context.args[1]) if len(context.args) > 1 else 2
        
        add_admin(target_id, level=level)
        
        text = f"✅ کاربر {target_id} به ادمین سطح {level} ارتقا یافت" if lang == "fa" else f"✅ User {target_id} promoted to admin level {level}"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        
    except ValueError:
        text = "❌ آیدی کاربر و سطح باید عدد باشند" if lang == "fa" else "❌ User ID and level must be numbers"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

async def admin_lock_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """قفل کردن کاربر"""
    uid = update.effective_user.id
    if not is_admin(uid):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Access denied.")
        return
    
    user_data = get_user(uid) or {}
    lang = user_data.get("lang", "fa")
    
    if not context.args:
        text = "🔒 لطفاً آیدی کاربر را وارد کنید: /lockuser <user_id>" if lang == "fa" else "🔒 Please enter user ID: /lockuser <user_id>"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return
    
    try:
        target_id = int(context.args[0])
        
        # قفل کردن کاربر
        users = load_json("telegram_bot/data/users.json")
        if str(target_id) in users:
            users[str(target_id)]["locked"] = True
            save_json("telegram_bot/data/users.json", users)
            
            # بروزرسانی دیتابیس
            target_user = get_user(target_id) or {}
            target_user["locked"] = True
            upsert_user(target_id, target_user)
            
            text = f"✅ کاربر {target_id} قفل شد" if lang == "fa" else f"✅ User {target_id} locked"
        else:
            text = "❌ کاربر یافت نشد" if lang == "fa" else "❌ User not found"
        
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        
    except ValueError:
        text = "❌ آیدی کاربر باید عدد باشد" if lang == "fa" else "❌ User ID must be a number"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

async def admin_unlock_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """باز کردن قفل کاربر"""
    uid = update.effective_user.id
    if not is_admin(uid):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Access denied.")
        return
    
    user_data = get_user(uid) or {}
    lang = user_data.get("lang", "fa")
    
    if not context.args:
        text = "🔓 لطفاً آیدی کاربر را وارد کنید: /unlockuser <user_id>" if lang == "fa" else "🔓 Please enter user ID: /unlockuser <user_id>"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return
    
    try:
        target_id = int(context.args[0])
        
        # باز کردن قفل کاربر
        users = load_json("telegram_bot/data/users.json")
        if str(target_id) in users:
            users[str(target_id)]["locked"] = False
            save_json("telegram_bot/data/users.json", users)
            
            # بروزرسانی دیتابیس
            target_user = get_user(target_id) or {}
            target_user["locked"] = False
            upsert_user(target_id, target_user)
            
            text = f"✅ کاربر {target_id} آزاد شد" if lang == "fa" else f"✅ User {target_id} unlocked"
        else:
            text = "❌ کاربر یافت نشد" if lang == "fa" else "❌ User not found"
        
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        
    except ValueError:
        text = "❌ آیدی کاربر باید عدد باشد" if lang == "fa" else "❌ User ID must be a number"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
