# telegram_bot/handlers/admin_codes_handlers.py
from telegram import Update
from telegram.ext import ContextTypes
from utils.database import is_admin, get_user
from utils.code_tools import generate_code, create_code
from utils.time_tools import now_utc, add_days, add_months, iso
from config.messages import get_text
import logging

LOG = logging.getLogger(__name__)

async def admin_generate_test_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """تولید کد تست یک روزه"""
    uid = update.effective_user.id
    if not is_admin(uid):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Access denied.")
        return
    
    user_data = get_user(uid) or {}
    lang = user_data.get("lang", "fa")
    
    code = generate_code()
    expires_at = add_days(now_utc(), 1)  # 1 روز
    
    # ذخیره کد
    create_code(code, "test", expires_at=iso(expires_at), max_uses=1, duration_days=1)
    
    if lang == "fa":
        text = f"""🧪 کد تست یک روزه ساخته شد:

🔑 کد: `{code}`
⏰ مدت: 1 روز
📅 انقضا: {iso(expires_at)}
👥 تعداد استفاده: 1 بار"""
    else:
        text = f"""🧪 1-Day Test Code Generated:

🔑 Code: `{code}`
⏰ Duration: 1 day
📅 Expires: {iso(expires_at)}
👥 Uses: 1 time"""
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

async def admin_generate_1month_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """تولید کد اشتراک ۱ ماهه"""
    uid = update.effective_user.id
    if not is_admin(uid):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Access denied.")
        return
    
    user_data = get_user(uid) or {}
    lang = user_data.get("lang", "fa")
    
    code = generate_code()
    expires_at = add_months(now_utc(), 1)  # 1 ماه
    
    # ذخیره کد
    create_code(code, "1month", expires_at=iso(expires_at), max_uses=1, duration_days=30)
    
    if lang == "fa":
        text = f"""📅 کد اشتراک ۱ ماهه ساخته شد:

🔑 کد: `{code}`
⏰ مدت: 1 ماه
📅 انقضا: {iso(expires_at)}
👥 تعداد استفاده: 1 بار"""
    else:
        text = f"""📅 1-Month Subscription Code Generated:

🔑 Code: `{code}`
⏰ Duration: 1 month
📅 Expires: {iso(expires_at)}
👥 Uses: 1 time"""
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

async def admin_generate_3month_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """تولید کد اشتراک ۳ ماهه"""
    uid = update.effective_user.id
    if not is_admin(uid):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Access denied.")
        return
    
    user_data = get_user(uid) or {}
    lang = user_data.get("lang", "fa")
    
    code = generate_code()
    expires_at = add_months(now_utc(), 3)  # 3 ماه
    
    # ذخیره کد
    create_code(code, "3month", expires_at=iso(expires_at), max_uses=1, duration_days=90)
    
    if lang == "fa":
        text = f"""📅 کد اشتراک ۳ ماهه ساخته شد:

🔑 کد: `{code}`
⏰ مدت: 3 ماه
📅 انقضا: {iso(expires_at)}
👥 تعداد استفاده: 1 بار"""
    else:
        text = f"""📅 3-Month Subscription Code Generated:

🔑 Code: `{code}`
⏰ Duration: 3 months
📅 Expires: {iso(expires_at)}
👥 Uses: 1 time"""
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

async def admin_generate_4month_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """تولید کد اشتراک ۴ ماهه"""
    uid = update.effective_user.id
    if not is_admin(uid):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Access denied.")
        return
    
    user_data = get_user(uid) or {}
    lang = user_data.get("lang", "fa")
    
    code = generate_code()
    expires_at = add_months(now_utc(), 4)  # 4 ماه
    
    # ذخیره کد
    create_code(code, "4month", expires_at=iso(expires_at), max_uses=1, duration_days=120)
    
    if lang == "fa":
        text = f"""📅 کد اشتراک ۴ ماهه ساخته شد:

🔑 کد: `{code}`
⏰ مدت: 4 ماه
📅 انقضا: {iso(expires_at)}
👥 تعداد استفاده: 1 بار"""
    else:
        text = f"""📅 4-Month Subscription Code Generated:

🔑 Code: `{code}`
⏰ Duration: 4 months
📅 Expires: {iso(expires_at)}
👥 Uses: 1 time"""
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

async def admin_generate_gift_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """تولید کد هدیه"""
    uid = update.effective_user.id
    if not is_admin(uid):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Access denied.")
        return
    
    user_data = get_user(uid) or {}
    lang = user_data.get("lang", "fa")
    
    if not context.args:
        text = "🎁 لطفاً تعداد استفاده و مدت را وارد کنید: /giftcode <max_uses> <days>" if lang == "fa" else "🎁 Please enter max uses and days: /giftcode <max_uses> <days>"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return
    
    try:
        max_uses = int(context.args[0])
        days = int(context.args[1]) if len(context.args) > 1 else 30
        
        code = generate_code()
        expires_at = add_days(now_utc(), days)
        
        # ذخیره کد
        create_code(code, "gift", expires_at=iso(expires_at), max_uses=max_uses, duration_days=days)
        
        if lang == "fa":
            text = f"""🎁 کد هدیه ساخته شد:

🔑 کد: `{code}`
⏰ مدت: {days} روز
📅 انقضا: {iso(expires_at)}
👥 تعداد استفاده: {max_uses} بار"""
        else:
            text = f"""🎁 Gift Code Generated:

🔑 Code: `{code}`
⏰ Duration: {days} days
📅 Expires: {iso(expires_at)}
👥 Uses: {max_uses} times"""
        
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        
    except ValueError:
        text = "❌ تعداد استفاده و مدت باید عدد باشند" if lang == "fa" else "❌ Max uses and days must be numbers"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
