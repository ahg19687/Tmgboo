from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from utils.translation import LANG_LABEL, MESSAGES
from utils.user_tools import set_lang, load_users
from utils.ui_tools import inline_back_buttons
async def change_lang_button(update: Update, context):
    query = update.callback_query
    await query.answer()
    kb = [
        [InlineKeyboardButton(LANG_LABEL['fa'], callback_data='lang_fa'), InlineKeyboardButton(LANG_LABEL['en'], callback_data='lang_en')]
    ]
    await query.edit_message_text('Choose language / انتخاب زبان:', reply_markup=InlineKeyboardMarkup(kb + inline_back_buttons().keyboard))
async def set_lang_handler(update: Update, context):
    query = update.callback_query
    await query.answer()
    data = query.data
    uid = query.from_user.id
    if data == 'lang_fa':
        set_lang(uid, 'fa')
        msg = MESSAGES['fa']['lang_changed'].format(lang=LANG_LABEL['fa'])
    else:
        set_lang(uid, 'en')
        msg = MESSAGES['en']['lang_changed'].format(lang=LANG_LABEL['en'])
    await query.edit_message_text(msg)
