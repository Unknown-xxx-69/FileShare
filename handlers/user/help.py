from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup
from config import Messages, Buttons, BOT_NAME
import logging
import re

logger = logging.getLogger(__name__)

# Safely remove emojis and invalid surrogates
def safe_utf(text: str) -> str:
    emoji_and_surrogate_pattern = re.compile(
        "["
        "\U00010000-\U0010FFFF"  # Unicode emojis and supplementary chars
        "\ud800-\udfff"          # Invalid surrogate range
        "]+",
        flags=re.UNICODE
    )
    return emoji_and_surrogate_pattern.sub('', text)

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
