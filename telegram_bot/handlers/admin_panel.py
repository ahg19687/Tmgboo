# telegram_bot/handlers/admin_panel.py
from telegram import Update
from telegram.ext import ContextTypes
from utils.database import is_admin, list_users, get_user
from keyboards.admin_keyboards import admin_main_menu
import logging

LOG = logging.getLogger(__name__)

async def admin_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if not is_admin(uid):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Access denied.")
        return
    
    user_data = get_user(uid) or {}
    lang = user_data.get("lang", "fa")
    
    users = list_users()
    text = f"👑 Admin Panel\n📊 Users: {len(users)}\n🎯 Use the menu below to manage the system."
    
    if lang == "fa":
        text = f"👑 پنل مدیریت\n📊 کاربران: {len(users)}\n🎯 از منوی زیر برای مدیریت سیستم استفاده کنید."
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_markup=admin_main_menu(lang)
    )

# هندلر برای منوی اصلی ادمین
async def admin_main_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if not is_admin(uid):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Access denied.")
        return
    
    user_data = get_user(uid) or {}
    lang = user_data.get("lang", "fa")
    
    text = "👑 Admin Main Menu - Choose management section:"
    if lang == "fa":
        text = "👑 منوی اصلی مدیریت - بخش مورد نظر را انتخاب کنید:"
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_markup=admin_main_menu(lang)
    )
