# telegram_bot/handlers/profile.py
from telegram import Update
from telegram.ext import ContextTypes
from utils.database import get_user, is_admin
from utils.time_tools import remaining
from config.messages import get_text
from keyboards.user_keyboards import unlocked_user_menu
from keyboards.admin_keyboards import admin_main_menu
from keyboards.locked_user import get_locked_keyboard

async def profile_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    user_rec = get_user(uid) or {}
    lang = user_rec.get("lang", "fa")
    
    # اطلاعات کاربر
    sub = user_rec.get("subscription", {})
    if sub and sub.get("expires_at"):
        rem = remaining(sub.get("expires_at"))
        rem_str = f"{rem['days']} روز {rem['hours']} ساعت" if lang == "fa" else f"{rem['days']}d {rem['hours']}h"
    else:
        rem_str = "بدون اشتراک" if lang == "fa" else "No subscription"
    
    groups = len(user_rec.get("groups", []))
    locked = user_rec.get("locked", True)
    user_type = "ادمین" if is_admin(uid) else ("کاربر آزاد" if not locked else "کاربر قفل شده")
    
    if lang == "fa":
        text = f"""👤 پروفایل کاربر

🆔 آیدی: {uid}
👤 نوع: {user_type}
📅 اشتراک: {sub.get('type', '—')}
⏰ زمان باقی‌مانده: {rem_str}
👥 گروه‌ها: {groups} گروه
🌐 زبان: فارسی"""
    else:
        text = f"""👤 User Profile

🆔 ID: {uid}
👤 Type: {user_type}
📅 Subscription: {sub.get('type', '—')}
⏰ Remaining: {rem_str}
👥 Groups: {groups} groups
🌐 Language: English"""
    
    # انتخاب کیبورد مناسب
    if is_admin(uid):
        keyboard = admin_main_menu(lang)
    elif not locked:
        keyboard = unlocked_user_menu(lang)
    else:
        keyboard = get_locked_keyboard(lang)
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_markup=keyboard
                               )
