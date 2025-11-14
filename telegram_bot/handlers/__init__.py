# telegram_bot/handlers/__init__.py
from telegram.ext import CommandHandler, MessageHandler, filters, CallbackQueryHandler
from . import (start, language, support, unlock_system, profile, admin_panel, 
               admin_users, admin_codes, user_groups, message_scheduler, 
               reminders, misc_callbacks, navigation, admin_users_handlers,
               admin_codes_handlers, admin_admins_handlers, admin_messages_handlers,
               user_messages_handlers)

def register_handlers(app):
    # commands
    app.add_handler(CommandHandler("start", start.start_cmd))
    app.add_handler(CommandHandler("profile", profile.profile_cmd))
    app.add_handler(CommandHandler("mygroups", user_groups.list_groups_cmd))
    app.add_handler(CommandHandler("unlock", unlock_system.unlock_cmd))
    app.add_handler(CommandHandler("schedule", message_scheduler.schedule_cmd))
    
    # user groups commands
    app.add_handler(CommandHandler("addgroup", user_groups.add_group_cmd))
    app.add_handler(CommandHandler("removegroup", user_groups.remove_group_cmd))
    
    # user messages commands
    app.add_handler(CommandHandler("send", user_messages_handlers.user_instant_send))
    app.add_handler(CommandHandler("toadmin", user_messages_handlers.user_message_to_admin))
    
    # ✅ اصلاح شده: حذف هندلر مشکل‌ساز و استفاده از هندلر جدید پشتیبانی
    # هندلر پیام‌های متنی حالا در support.py ثبت می‌شه
    
    # navigation handlers
    start.register_navigation_handlers(app)
    
    # callbacks
    app.add_handler(CallbackQueryHandler(misc_callbacks.callback_router))
    
    # admin commands
    app.add_handler(CommandHandler("admin", admin_panel.admin_cmd))
    app.add_handler(CommandHandler("addadmin", admin_users.add_admin_cmd))
    app.add_handler(CommandHandler("gencode", admin_codes.gen_code_cmd))
    
    # admin users commands
    app.add_handler(CommandHandler("listusers", admin_users_handlers.admin_list_users))
    app.add_handler(CommandHandler("searchuser", admin_users_handlers.admin_search_user))
    app.add_handler(CommandHandler("promote", admin_users_handlers.admin_promote_user))
    app.add_handler(CommandHandler("lockuser", admin_users_handlers.admin_lock_user))
    app.add_handler(CommandHandler("unlockuser", admin_users_handlers.admin_unlock_user))
    
    # admin codes commands
    app.add_handler(CommandHandler("testcode", admin_codes_handlers.admin_generate_test_code))
    app.add_handler(CommandHandler("1monthcode", admin_codes_handlers.admin_generate_1month_code))
    app.add_handler(CommandHandler("3monthcode", admin_codes_handlers.admin_generate_3month_code))
    app.add_handler(CommandHandler("4monthcode", admin_codes_handlers.admin_generate_4month_code))
    app.add_handler(CommandHandler("giftcode", admin_codes_handlers.admin_generate_gift_code))
    
    # admin admins commands
    app.add_handler(CommandHandler("listadmins", admin_admins_handlers.admin_list_admins))
    app.add_handler(CommandHandler("removeadmin", admin_admins_handlers.admin_remove_admin))
    
    # admin messages commands
    app.add_handler(CommandHandler("broadcast", admin_messages_handlers.admin_broadcast_message))
    app.add_handler(CommandHandler("senduser", admin_messages_handlers.admin_send_to_user))
    
    # ✅ اضافه شده: ثبت هندلرهای پشتیبانی
    support.register_support_handlers(app)
    
    # group updates - FIXED: استفاده از CHAT_MEMBER به جای MY_CHAT_MEMBER
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS | filters.StatusUpdate.LEFT_CHAT_MEMBER, user_groups.my_chat_member_update))
