from pyrogram import Client, filters
from pyrogram.types import Message
from utils import ButtonManager

button_manager = ButtonManager()

@Client.on_message(filters.command("help"))
async def help_command(client: Client, message: Message):
    help_text = (
        "<b>📚 Bot Commands & Usage</b>\n\n"
        "<i>Here are the available commands:</i>\n\n"
        
        "<b>👤 User Commands:</b>\n"
        "• /start - Start the bot\n"
        "• /help - Show this help message\n"
        "• /about - About the bot\n\n"
        
        "<b>👮 Admin Commands:</b>\n"
        "• /upload - Upload a file (reply to a file)\n"
        "• /auto_del - Set auto-delete time\n"
        "• /stats - View bot statistics\n"
        "• /bcast - Broadcast message to users\n\n"

        "<b>🗑️ Auto-Delete Feature:</b>\n"
        "Files are automatically deleted after the set time.\n"
        "Use /auto_del to change the deletion time.\n\n"
        
        "<b>🔗 Link Shortener:</b>\n"
        "Use /short to shorten any URL.\n"
        "<i>Example:</i> /short https://example.com"
    )

    await message.reply_text(
        help_text,
        reply_markup=button_manager.help_button(),
        parse_mode="html"
    )
