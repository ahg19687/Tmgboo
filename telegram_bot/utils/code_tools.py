# telegram_bot/utils/code_tools.py
# code generate and validate

import random, string
from utils.database import load_unlock_codes, save_unlock_codes
from utils.time_tools import now_utc, iso

def generate_code(length=6):
    chars = string.ascii_uppercase + string.digits
    return "".join(random.choice(chars) for _ in range(length))

def create_bulk_codes(n, typ="1m", duration_days=30, issued_by=None, max_uses=1):
    codes = load_unlock_codes()
    out = []
    for _ in range(n):
        c = generate_code()
        obj = {
            "code": c,
            "type": typ,
            "duration_days": duration_days,
            "issued_by": issued_by,
            "issued_at": iso(now_utc()),
            "expires_at": None,
            "used_by": None,
            "used_at": None,
            "max_uses": max_uses,
            "uses": 0
        }
        codes.append(obj)
        out.append(obj)
    save_unlock_codes(codes)
    return out

def validate_code(code_str, user_id):
    codes = load_unlock_codes()
    for c in codes:
        if c["code"] == code_str:
            # check expiry
            if c.get("expires_at"):
                # parse if necessary (not fully implemented)
                pass
            if c.get("uses",0) >= c.get("max_uses",1):
                return {"ok": False, "reason": "used"}
            # compute expires_at
            from utils.time_tools import add_days, iso
            expires = iso(add_days(now_utc(), c.get("duration_days",1)))
            return {"ok": True, "type": c.get("type","test"), "expires_at": expires}
    return {"ok": False, "reason": "notfound"}

def consume_code(code_str, user_id):
    codes = load_unlock_codes()
    for c in codes:
        if c["code"] == code_str:
            c["uses"] = c.get("uses",0) + 1
            if c["uses"] >= c.get("max_uses",1):
                c["used_by"] = user_id
                c["used_at"] = iso(now_utc())
            save_unlock_codes(codes)
            return True
    return False

# اضافه کردن فانکشن list_codes
def list_codes(active_only=True):
    """لیست تمام کدها - اگر active_only=True فقط کدهای استفاده نشده رو برمی‌گرداند"""
    codes = load_unlock_codes()
    if active_only:
        active_codes = []
        for code in codes:
            if code.get("uses", 0) < code.get("max_uses", 1):
                active_codes.append(code)
        return active_codes
    return codes

# اضافه کردن تابع create_code
def create_code(code, code_type, expires_at=None, max_uses=1, duration_days=None, issued_by=None):
    """ذخیره کد جدید در دیتابیس"""
    codes = load_unlock_codes()
    
    # محاسبه expires_at اگر duration_days داده شده
    if duration_days and not expires_at:
        from utils.time_tools import add_days, iso
        expires_at = iso(add_days(now_utc(), duration_days))
    
    # محاسبه duration_days بر اساس نوع کد
    if not duration_days:
        if code_type == "test":
            duration_days = 1
        elif code_type == "1month":
            duration_days = 30
        elif code_type == "3month":
            duration_days = 90
        elif code_type == "4month":
            duration_days = 120
        else:  # gift یا سایر انواع
            duration_days = 30
    
    # ایجاد آبجکت کد
    code_obj = {
        "code": code,
        "type": code_type,
        "duration_days": duration_days,
        "issued_by": issued_by,
        "issued_at": iso(now_utc()),
        "expires_at": expires_at,
        "used_by": None,
        "used_at": None,
        "max_uses": max_uses,
        "uses": 0
    }
    
    codes.append(code_obj)
    save_unlock_codes(codes)
    return code_obj
