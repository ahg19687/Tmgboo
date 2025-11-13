# telegram_bot/handlers/unlock_system.py

from telegram import Update
from telegram.ext import ContextTypes
from utils.code_tools import validate_code, consume_code
from utils.database import upsert_user, get_user
from utils.time_tools import iso
from config.messages import get_text
from utils.json_tools import load_json, save_json   # 🔹 اضافه شد

async def unlock_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    args = context.args

    if not args:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Usage: /unlock <CODE>")
        return

    code = args[0].strip().upper()
    res = validate_code(code, user_id)

    if not res["ok"]:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=get_text("invalid_code", lang=get_user(user_id).get("lang", "fa"))
        )
        return

    # ✅ کد معتبر است
    consume_code(code, user_id)

    user_rec = get_user(user_id) or {"user_id": user_id}
    user_rec["subscription"] = {"expires_at": res["expires_at"], "type": res["type"]}
    upsert_user(user_id, user_rec)

    # --- 🔹 این قسمت جدید اضافه شد ---
    users = load_json("telegram_bot/data/users.json")
    if str(user_id) in users:
        users[str(user_id)]["locked"] = False
    else:
        users[str(user_id)] = {"locked": False}
    save_json("telegram_bot/data/users.json", users)
    # -----------------------------------

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=get_text("unlock_success", lang=user_rec.get("lang", "fa"), expires=res["expires_at"])
    )
