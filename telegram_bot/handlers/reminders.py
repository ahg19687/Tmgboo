# telegram_bot/handlers/reminders.py

from utils.database import list_users, upsert_user
from utils.time_tools import now_utc, parse_iso
from config.config import SETTINGS
import logging

LOG = logging.getLogger(__name__)

def reminders_job(bot):
    users = list_users()
    days = SETTINGS.get("reminder_days_before_expiry", [7,1])
    for u in users:
        sub = u.get("subscription")
        if not sub: continue
        expires = parse_iso(sub.get("expires_at"))
        delta_days = (expires - now_utc()).days
        if delta_days in days:
            try:
                bot.send_message(chat_id=u["user_id"], text=f"Subscription expires in {delta_days} days.")
            except Exception as e:
                LOG.warning("reminder failed for %s: %s", u["user_id"], str(e))
