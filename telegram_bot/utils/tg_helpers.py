# telegram_bot/utils/tg_helpers.py
# safe send wrappers and keyboard helpers

import time
import logging
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.error import RetryAfter, Forbidden, BadRequest

LOG = logging.getLogger(__name__)

async def safe_send_message(bot, chat_id, text=None, photo=None, **kwargs):
    try:
        if photo:
            return await bot.send_photo(chat_id=chat_id, photo=photo, caption=text, **kwargs)
        return await bot.send_message(chat_id=chat_id, text=text, **kwargs)
    except RetryAfter as e:
        wait = e.retry_after + 1
        LOG.info("RetryAfter: waiting %s", wait)
        time.sleep(wait)
        return await safe_send_message(bot, chat_id, text, photo, **kwargs)
    except (Forbidden, BadRequest) as e:
        LOG.warning("unable to send to %s: %s", chat_id, str(e))
        return None
    except Exception as e:
        LOG.error("send_message error: %s", str(e))
        return None

def make_inline(rows):
    return InlineKeyboardMarkup([[InlineKeyboardButton(t, callback_data=d) for t,d in row] for row in rows])
