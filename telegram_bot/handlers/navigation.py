# telegram_bot/handlers/navigation.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.database import get_user, is_admin
from config.messages import get_text
from keyboards.admin_keyboards import admin_main_menu
from keyboards.user_keyboards import unlocked_user_menu

async def go_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = get_user(update.effective_user.id) or {}
    lang = user_data.get("lang", "fa")
    locked = user_data.get("locked", True)
    admin = is_admin(update.effective_user.id)

    # اگر کاربر ادمین باشد، منوی ادمین نشان داده شود
    if admin:
        text = "👑 Admin Panel - Choose management section:"
        if lang == "fa":
            text = "👑 پنل مدیریت - بخش مورد نظر را انتخاب کنید:"
        
        if update.message:
            await update.message.reply_text(
                text=text,
                reply_markup=admin_main_menu(lang)
            )
        else:
            await update.callback_query.edit_message_text(
                text=text,
                reply_markup=admin_main_menu(lang)
            )
        return

    # کاربران عادی
    if locked:
        text = get_text("start_locked", lang=lang)
        keyboard = [
            [InlineKeyboardButton(get_text("menu_language", lang=lang), callback_data="lang")],
            [InlineKeyboardButton(get_text("menu_unlock", lang=lang), callback_data="unlock")],
            [InlineKeyboardButton(get_text("menu_support", lang=lang), callback_data="support")],
        ]
    else:
        text = get_text("start_unlocked", lang=lang)
        keyboard = [
            [InlineKeyboardButton(get_text("menu_language", lang=lang), callback_data="lang")],
            [InlineKeyboardButton(get_text("menu_my_groups", lang=lang), callback_data="my_groups")],
            [InlineKeyboardButton(get_text("menu_scheduler", lang=lang), callback_data="scheduler")],
            [InlineKeyboardButton(get_text("menu_send_now", lang=lang), callback_data="send_now")],
            [InlineKeyboardButton(get_text("menu_profile", lang=lang), callback_data="profile")],
            [InlineKeyboardButton(get_text("back_to_main", lang=lang), callback_data="main_menu")],
        ]

    if update.message:
        await update.message.reply_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.callback_query.edit_message_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
