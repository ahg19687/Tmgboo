# telegram_bot/utils/scheduler.py
# APScheduler wrapper

from apscheduler.schedulers.background import BackgroundScheduler
from config.config import SETTINGS
from utils.database import list_scheduled_messages
import logging, asyncio
LOG = logging.getLogger(__name__)

_scheduler = BackgroundScheduler()

def start_scheduler(app=None):
    if not _scheduler.running:
        _scheduler.start()
    # schedule daily reminders
    daily_time = SETTINGS.get("daily_send_time", "09:00")
    hour, minute = map(int, daily_time.split(":"))
    _scheduler.add_job(lambda: LOG.info("daily job trigger"), 'cron', hour=hour, minute=minute, id="daily_send")
    LOG.info("Scheduler started")

def schedule_message_job(obj):
    # obj contains time HH:MM and id
    time_str = obj.get("time")
    hour, minute = map(int, time_str.split(":"))
    _scheduler.add_job(lambda: _run_send(obj), 'cron', hour=hour, minute=minute, id=f"msg_{obj.get('id')}")
    LOG.info("Scheduled message job for %s at %s", obj.get("owner_id"), time_str)

def _run_send(obj):
    # This is a sync placeholder — actual implementation should use bot instance
    LOG.info("Running scheduled send for %s", obj.get("id"))
    # TODO: integrate with bot to send message to groups
