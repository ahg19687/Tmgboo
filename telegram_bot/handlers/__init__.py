# telegram_bot/handlers/__init__.py

from telegram.ext import CommandHandler, MessageHandler, filters, CallbackQueryHandler
from . import start, language, support, unlock_system, profile, admin_panel, user_groups, message_scheduler, reminders, misc_callbacks, navigation

def register_handlers(app):
    # commands
    app.add_handler(CommandHandler("start", start.start_cmd))
    app.add_handler(CommandHandler("profile", profile.profile_cmd))
    app.add_handler(CommandHandler("mygroups", user_groups.list_groups_cmd))
    
    # message handlers
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, support.text_message))
    
    # navigation handlers
    start.register_navigation_handlers(app)
    
    # callbacks - باید این هندلر رو به misc_callbacks.callback_router اضافه کنی
    app.add_handler(CallbackQueryHandler(misc_callbacks.callback_router))
    
    # admin commands
    app.add_handler(CommandHandler("admin", admin_panel.admin_cmd))
