# telegram_bot/utils/time_tools.py
# time helpers

from datetime import datetime, timezone, timedelta
import calendar

def now_utc():
    return datetime.now(timezone.utc)

def iso(dt):
    if isinstance(dt, (int, float)):
        dt = datetime.fromtimestamp(dt, timezone.utc)
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00","Z")

def parse_iso(s):
    try:
        return datetime.fromisoformat(s.replace("Z","+00:00"))
    except Exception:
        return None

def remaining(expires_iso):
    exp = parse_iso(expires_iso)
    if not exp:
        return {"days":0,"hours":0,"minutes":0}
    delta = exp - now_utc()
    days = max(delta.days, 0)
    hours = max(delta.seconds // 3600, 0)
    minutes = max((delta.seconds % 3600) // 60, 0)
    return {"days": days, "hours": hours, "minutes": minutes}

def add_days(dt, days):
    return dt + timedelta(days=days)

# اضافه کردن تابع add_months
def add_months(date, months):
    """اضافه کردن ماه به تاریخ"""
    month = date.month - 1 + months
    year = date.year + month // 12
    month = month % 12 + 1
    day = min(date.day, calendar.monthrange(year, month)[1])
    return date.replace(year=year, month=month, day=day)
