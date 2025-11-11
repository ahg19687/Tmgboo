from telegram import Update
from utils.database import load_json
from utils.translation import MESSAGES
from utils.ui_tools import inline_back_buttons
ADMINS_FILE = 'data/admins.json'
def get_admins_text():
    admins = load_json(ADMINS_FILE, {})
    if not admins:
        return 'No admins set.'
    lines = []
    for uid, meta in admins.items():
        if meta.get('username'):
            lines.append(f"@{meta['username']}")
        else:
            lines.append(str(uid))
    return "\n".join(lines)
async def show_support(update: Update, context):
    query = update.callback_query if update.callback_query else None
    user = update.effective_user
    from utils.user_tools import load_users
    users = load_users()
    lang = users.get(str(user.id), {}).get('lang', 'fa')
    msg_tpl = MESSAGES[lang]['support_prompt']
    admins = get_admins_text()
    text = msg_tpl.format(admins=admins)
    kb = inline_back_buttons()
    if query:
        await query.answer()
        await query.edit_message_text(text, reply_markup=kb)
    else:
        await update.message.reply_text(text, reply_markup=kb)
