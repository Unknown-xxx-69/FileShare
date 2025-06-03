from pyrogram import Client, filters
from pyrogram.types import Message
from utils import ButtonManager
import logging

logger = logging.getLogger(__name__)
button_manager = ButtonManager()

def safe_utf(text: str) -> str:
    # Removes invalid UTF-16 surrogate pairs to prevent UnicodeEncodeError
    return ''.join(c for c in text if not (0xD800 <= ord(c) <= 0xDFFF))

@Client.on_message(filters.command("help"))
async def help_command(client: Client, message: Message):
    try:
        help_text = (
            "╭───〔 **📚 Bot Commands & Usage** 〕───⍟\n\n"
            "👥 **User Commands**\n"
            "├• `/start` — Start the bot\n"
            "├• `/help` — Show this help message\n"
            "└• `/about` — About the bot\n\n"
            "👑 **Admin Commands**\n"
            "├• `/upload` — Upload a file (reply to file)\n"
            "├• `/auto_del` — Set auto-delete time\n"
            "├• `/stats` — View bot statistics\n"
            "├• `/bcast` — Broadcast message to all users\n"
            "└• `/bcast_time` — Toggle timed broadcast\n\n"
            "💡 **Auto-Delete Feature**\n"
            "Files are auto-deleted after a set time.\n"
            "Use `/auto_del` to configure it.\n\n"
            "🔗 **URL Shortener**\n"
            "Use `/short <URL>` to shorten links using InshortURL.\n\n"
            "╰─────────────⍟"
        )

        await message.reply_text(safe_utf(help_text), reply_markup=button_manager.help_button())
    except Exception as e:
        logger.error(f"[HELP CMD ERROR] User: {message.from_user.id} | Error: {e}")
