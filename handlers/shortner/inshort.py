from pyrogram import Client, filters
from pyrogram.types import Message
import httpx
import logging
import re
import config  # Make sure LS_API_KEY and ADMIN_IDS are defined

logger = logging.getLogger(__name__)

# Validate API key on load
if not getattr(config, "LS_API_KEY", "").strip():
    raise ValueError("❌ InshortURL API key (LS_API_KEY) is missing in config.py.")

INSHORT_API_URL = "https://inshorturl.com/api"
URL_PATTERN = re.compile(r'^https?://[^\s]+$')


@Client.on_message(filters.command("short") & filters.user(config.ADMIN_IDS))
async def short_url_command(client: Client, message: Message):
    """
    Command: /short <url>
    Description: Shortens a URL using the InshortURL API.
    Only accessible by admin users defined in config.ADMIN_IDS.
    """
    try:
        parts = message.text.split(maxsplit=1)
        if len(parts) != 2:
            await message.reply_text(
                "❌ **Invalid command format!**\n\n"
                "**Usage:** `/short <url>`\n"
                "**Example:** `/short https://example.com`",
                quote=True
            )
            return

        url = parts[1].strip()

        if not URL_PATTERN.match(url):
            await message.reply_text(
                "❌ **Invalid URL format.**\nMake sure the URL starts with `http://` or `https://`.",
                quote=True
            )
            return

        status_msg = await message.reply_text("🔄 **Processing your URL...**", quote=True)

        params = {
            "api": config.LS_API_KEY,
            "url": url
        }

        async with httpx.AsyncClient() as client_http:
            response = await client_http.get(INSHORT_API_URL, params=params)
            response.raise_for_status()
            data = response.json()  # ✅ FIXED: removed await

        if data.get("status") == "success":
            shortened_url = data.get("shortenedUrl")

            await status_msg.edit_text(
                f"✅ **URL Shortened Successfully!**\n\n"
                f"**Original URL:**\n`{url}`\n\n"
                f"**Shortened URL:**\n`{shortened_url}`\n\n"
                f"🔗 Powered by @Priyaverma2004"
            )
        else:
            await status_msg.edit_text(
                f"❌ **Failed to shorten URL!**\n\n"
                f"**Reason:** `{data.get('message', 'Unknown error.')}`"
            )

    except httpx.HTTPError as e:
        logger.exception("HTTP error during URL shortening")
        await message.reply_text(
            f"❌ **API Error:**\n`{str(e)}`\n\nPlease try again later.",
            quote=True
        )
    except Exception as e:
        logger.exception("Unexpected error in /short command")
        await message.reply_text(
            f"❌ **An unexpected error occurred:**\n`{str(e)}`",
            quote=True
        )
