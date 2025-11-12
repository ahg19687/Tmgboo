# telegram_bot/main.py
# application entry point

import os, logging
from telegram.ext import ApplicationBuilder
from handlers import register_handlers
from utils.scheduler import start_scheduler
from keep_alive import start_keep_alive
from config.config import SETTINGS

logging.basicConfig(level=SETTINGS.get("log_level","INFO"))
LOG = logging.getLogger(__name__)

def main():
    token = os.getenv("BOT_TOKEN") or SETTINGS.get("bot_token")
    if not token:
        LOG.error("BOT_TOKEN not set. Exiting.")
        return
    app = ApplicationBuilder().token(token).build()
    register_handlers(app)
    # start scheduler (background)
    start_scheduler(app)
    # start keepalive flask
    start_keep_alive()
    LOG.info("Starting polling...")
    app.run_polling()

if __name__ == "__main__":
    main()
