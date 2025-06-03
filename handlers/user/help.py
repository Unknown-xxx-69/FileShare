from pyrogram import Client, filters
from pyrogram.types import Message
from utils import ButtonManager

button_manager = ButtonManager()

@Client.on_message(filters.command("help"))
async def help_command(client: Client, message: Message):
    help_text = (
        "**Bot Commands & Usage**\n\n"
        "Here are the available commands:\n\n"
        "**User Commands:**\n"
        "• /start - Start the bot\n"
        "• /help - Show this help message\n"
        "• /about - About the bot\n\n"
        "**Admin Commands:**\n"
        "• /upload - Upload a file (reply to file)\n"
        "• /auto_del - Set auto-delete time\n"
        "• /stats - View bot statistics\n"
        "• /bcast - Broadcast message to users\n"
        "**Auto-Delete Feature:**\n"
        "Files are automatically deleted after the set time.\n"
        "Use /auto_del to change the deletion time.\n\n"
        "**Link Shortener:**\n"
        "Use /short to shorten any URL. Syntax: `/short https://example.com`"
    )
    await message.reply_text(help_text, reply_markup=button_manager.help_button(), parse_mode="Markdown")
