# telegram_bot/handlers/misc_callbacks.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config.messages import get_text
from utils.database import get_user, upsert_user

async def callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    user = update.effective_user
    
    # گرفتن زبان کاربر
    user_data = get_user(user.id) or {}
    lang = user_data.get("lang", "fa")
    
    await query.answer()

    if data == "lang":
        # منوی انتخاب زبان
        keyboard = [
            [InlineKeyboardButton("🇮🇷 فارسی", callback_data="setlang_fa")],
            [InlineKeyboardButton("🇺🇸 English", callback_data="setlang_en")],
            [InlineKeyboardButton(get_text("back_previous", lang=lang), callback_data="back_prev")],
            [InlineKeyboardButton(get_text("back_to_main", lang=lang), callback_data="main_menu")]
        ]
        await query.edit_message_text(
            text=get_text("choose_language", lang=lang),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        
    elif data.startswith("setlang_"):
        # تغییر زبان
        new_lang = data.replace("setlang_", "")
        user_data["lang"] = new_lang
        upsert_user(user.id, user_data)
        
        await query.edit_message_text(
            text=get_text("lang_changed", lang=new_lang)  # ✅ اینجا درست شده
        )
        
    elif data == "unlock":
        await query.edit_message_text(
            text=get_text("ask_code", lang=lang)
        )
        
    elif data == "support":
        from .support import get_support_message
        support_text = await get_support_message(user.id, lang)
        await query.edit_message_text(
            text=support_text
        )
        
    elif data == "profile":
        from .profile import profile_cmd
        await profile_cmd(update, context)
        
    elif data == "my_groups":
        from .user_groups import list_groups_cmd
        await list_groups_cmd(update, context)
        
    elif data == "scheduler":
        from .message_scheduler import scheduler_menu
        await scheduler_menu(update, context)
        
    elif data == "send_now":
        from .message_scheduler import send_now_menu
        await send_now_menu(update, context)
        
    elif data in ["back_prev", "main_menu"]:
        from .navigation import go_back
        await go_back(update, context)
        
    else:
        await query.edit_message_text(
            text=get_text("unknown_action", lang=lang) or "❌ عمل ناشناخته"
                                 )
