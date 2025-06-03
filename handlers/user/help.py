from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup
from config import Messages, Buttons, BOT_NAME
import logging

logger = logging.getLogger(__name__)

def safe_utf(text: str) -> str:
    # Removes invalid UTF-16 surrogate pairs to prevent UnicodeEncodeError
    return ''.join(c for c in text if not (0xD800 <= ord(c) <= 0xDFFF))

@Client.on_message(filters.command("help"))
async def help_command(client: Client, message: Message):
    try:
        help_text = safe_utf(Messages.HELP_TEXT.format(bot_name=BOT_NAME))
        await message.reply_text(
            help_text,
            reply_markup=InlineKeyboardMarkup(Buttons.help_buttons())
        )
    except Exception as e:
        logger.error(f"[HELP CMD ERROR] User: {message.from_user.id} | Error: {e}")
