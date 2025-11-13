# telegram_bot/handlers/user_groups.py
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from utils.database import add_group_for_user, get_user, remove_group_for_user
from config.messages import get_text
from keyboards.user_keyboards import user_groups_menu

async def list_groups_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    u = get_user(uid) or {}
    lang = u.get("lang", "fa")
    groups = u.get("groups", [])
    
    if not groups:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text=get_text("no_groups", lang=lang),
            reply_markup=user_groups_menu(lang)
        )
        return
    
    if lang == "fa":
        txt = "📋 گروه‌های شما:\n\n"
        for i, group_id in enumerate(groups, 1):
            txt += f"{i}. آیدی گروه: {group_id}\n"
    else:
        txt = "📋 Your Groups:\n\n"
        for i, group_id in enumerate(groups, 1):
            txt += f"{i}. Group ID: {group_id}\n"
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=txt,
        reply_markup=user_groups_menu(lang)
    )

async def add_group_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """اضافه کردن گروه"""
    uid = update.effective_user.id
    user_data = get_user(uid) or {}
    lang = user_data.get("lang", "fa")
    
    if not context.args:
        text = "➕ لطفاً آیدی گروه را وارد کنید: /addgroup <group_id>" if lang == "fa" else "➕ Please enter group ID: /addgroup <group_id>"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return
    
    try:
        group_id = int(context.args[0])
        add_group_for_user(uid, group_id, title=f"Group {group_id}")
        
        text = f"✅ گروه {group_id} با موفقیت اضافه شد" if lang == "fa" else f"✅ Group {group_id} added successfully"
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            reply_markup=user_groups_menu(lang)
        )
        
    except ValueError:
        text = "❌ آیدی گروه باید عدد باشد" if lang == "fa" else "❌ Group ID must be a number"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

async def remove_group_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """حذف گروه"""
    uid = update.effective_user.id
    user_data = get_user(uid) or {}
    lang = user_data.get("lang", "fa")
    
    if not context.args:
        text = "🗑 لطفاً آیدی گروه را وارد کنید: /removegroup <group_id>" if lang == "fa" else "🗑 Please enter group ID: /removegroup <group_id>"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return
    
    try:
        group_id = int(context.args[0])
        remove_group_for_user(uid, group_id)
        
        text = f"✅ گروه {group_id} با موفقیت حذف شد" if lang == "fa" else f"✅ Group {group_id} removed successfully"
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            reply_markup=user_groups_menu(lang)
        )
        
    except ValueError:
        text = "❌ آیدی گروه باید عدد باشد" if lang == "fa" else "❌ Group ID must be a number"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

async def groups_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """منوی مدیریت گروه‌ها"""
    uid = update.effective_user.id
    user_data = get_user(uid) or {}
    lang = user_data.get("lang", "fa")
    
    if user_data.get("locked", True):
        text = "🔒 حساب شما قفل است. لطفاً اول قفل‌گشایی کنید." if lang == "fa" else "🔒 Your account is locked. Please unlock first."
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return
    
    text = """👥 منوی مدیریت گروه‌ها

دستورات موجود:
📋 /mygroups - نمایش گروه‌های من
➕ /addgroup <group_id> - اضافه کردن گروه
🗑 /removegroup <group_id> - حذف گروه

💡 نکته: بات باید در گروه ادمین باشد تا بتواند پیام ارسال کند.""" if lang == "fa" else """👥 Groups Management Menu

Available commands:
📋 /mygroups - Show my groups
➕ /addgroup <group_id> - Add group
🗑 /removegroup <group_id> - Remove group

💡 Note: The bot must be admin in the group to send messages."""
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_markup=user_groups_menu(lang)
    )

# my_chat_member handler to register group when bot added
async def my_chat_member_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        chat = update.my_chat_member.chat
        if update.my_chat_member.new_chat_member.status in ("member","administrator"):
            # register group with no owner
            add_group_for_user(None, chat.id, title=chat.title or "")
    except Exception:
        pass
