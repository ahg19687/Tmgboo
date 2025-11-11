from telegram import Update
from utils.code_tools import verify_and_consume
from utils.user_tools import grant_subscription, ensure_user, load_users
from utils.translation import MESSAGES
from utils.time_tools import dt_to_readable
from datetime import datetime
from utils.ui_tools import inline_back_buttons
async def unlock_command(update: Update, context):
    user = update.effective_user
    ensure_user(user.id, user.username, user.first_name, user.last_name)
    args = context.args
    users = load_users()
    lang = users.get(str(user.id), {}).get('lang', 'fa')
    async def safe_reply(text: str):
        if update.message:
            await update.message.reply_text(text, reply_markup=inline_back_buttons())
        elif update.callback_query:
            await update.callback_query.message.reply_text(text, reply_markup=inline_back_buttons())
            await update.callback_query.answer()
        elif update.effective_chat:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    if not args:
        await safe_reply(MESSAGES[lang]['ask_code'])
        return
    code = args[0].strip()
    ok, res = verify_and_consume(code, user.id)
    if not ok:
        await safe_reply(MESSAGES[lang]['code_invalid'])
        return
    duration = int(res.get('duration_days', 30))
    grant_subscription(user.id, duration)
    users = load_users()
    until = users[str(user.id)].get('expires')
    readable_date = dt_to_readable(datetime.fromisoformat(until))
    await safe_reply(MESSAGES[lang]['code_ok'].format(until=readable_date))
