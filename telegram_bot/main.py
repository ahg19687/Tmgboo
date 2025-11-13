# 📄 /telegram_bot/main.py
# Application entry point

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import os, logging
from telegram.ext import ApplicationBuilder
from handlers import register_handlers
from handlers.start import register_navigation_handlers  # Added
from utils.scheduler import start_scheduler
from keep_alive import start_keep_alive
from config.config import SETTINGS

logging.basicConfig(level=SETTINGS.get("log_level", "INFO"))
LOG = logging.getLogger(__name__)

def main():
    token = os.getenv("BOT_TOKEN") or SETTINGS.get("bot_token")
    if not token:
        LOG.error("BOT_TOKEN not set. Exiting.")
        return

    app = ApplicationBuilder().token(token).build()

    # ✅ register all handlers
    register_handlers(app)
    register_navigation_handlers(app)  # Added

    # ✅ start background scheduler
    start_scheduler(app)

    # ✅ start flask keepalive service
    start_keep_alive()

    LOG.info("Starting polling...")
    app.run_polling()

if __name__ == "__main__":
    main()
