import logging, os
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from handlers.start import handle_start
from handlers.language import change_lang_button, set_lang_handler
from handlers.support import show_support
from handlers.user_group_manager import my_groups, remove_group_cb
from handlers.admin_group_manager import show_user_groups
from handlers.admin_panel import show_admin_panel, admin_panel_callback, handle_admin_text, notif_callback
from handlers.reminders import process_expirations
from handlers.message_scheduler import send_message_to_all
from handlers.unlock import unlock_command
from handlers.admin_code_manager import admin_generate_code
from handlers.admin_find_user import find_user_cmd
from handlers.admin_notifications import notif_panel, toggle_notif_cb
import asyncio, logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
BOT_TOKEN = os.getenv('BOT_TOKEN') or ''
if not BOT_TOKEN:
    logger.error('BOT_TOKEN not set. Set it in Render environment variables.')
    raise SystemExit('BOT_TOKEN not set.')
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler('start', handle_start))
    app.add_handler(CommandHandler('unlock', unlock_command))
    app.add_handler(CommandHandler('mygroups', my_groups))
    app.add_handler(CommandHandler('usergroups', show_user_groups))
    app.add_handler(CommandHandler('admin', show_admin_panel))
    app.add_handler(CommandHandler('gen', admin_generate_code))
    app.add_handler(CommandHandler('finduser', find_user_cmd))
    app.add_handler(CommandHandler('notifpanel', notif_panel))
    app.add_handler(CallbackQueryHandler(change_lang_button, pattern='^change_lang$'))
    app.add_handler(CallbackQueryHandler(set_lang_handler, pattern='^lang_'))
    app.add_handler(CallbackQueryHandler(show_support, pattern='^support$'))
    app.add_handler(CallbackQueryHandler(remove_group_cb, pattern='^(remove_group|remove_all_groups)'))
    app.add_handler(CallbackQueryHandler(admin_panel_callback, pattern='^admin_'))
    app.add_handler(CallbackQueryHandler(notif_callback, pattern='^notif_'))
    app.add_handler(CallbackQueryHandler(toggle_notif_cb, pattern='^toggle_notif|'))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_admin_text))
    job_queue = app.job_queue
    async def check_expired(context):
        bot = context.bot
        await process_expirations(bot)
    async def broadcast_scheduled(context):
        bot = context.bot
        await send_message_to_all(bot)
    job_queue.run_repeating(check_expired, interval=3600, first=10)
    job_queue.run_repeating(broadcast_scheduled, interval=43200, first=60)
    logger.info('Bot started. Running polling...')
    app.run_polling()
if __name__ == '__main__':
    main()
