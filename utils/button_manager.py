from typing import List
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    InputMediaPhoto
)
import config
import logging

logger = logging.getLogger(__name__)

def remove_surrogates(text: str) -> str:
    return ''.join(c for c in text if not (0xD800 <= ord(c) <= 0xDFFF))

class ButtonManager:
    def __init__(self):
        self.force_sub_channels = [
            config.FORCE_SUB_CHANNEL,
            config.FORCE_SUB_CHANNEL_2,
            config.FORCE_SUB_CHANNEL_3,
            config.FORCE_SUB_CHANNEL_4
        ]
        self.db_channel = config.DB_CHANNEL_ID

    async def check_force_sub(self, client, user_id: int) -> bool:
        try:
            for ch_id in self.force_sub_channels:
                if ch_id != 0:
                    member = await client.get_chat_member(ch_id, user_id)
                    if member.status in ["left", "kicked"]:
                        return False
            return True
        except Exception as e:
            logger.error(f"Force sub check error for user {user_id}: {str(e).encode('utf-8', 'ignore').decode('utf-8')}")
            return False

    async def show_start(self, client, callback_query: CallbackQuery):
        try:
            caption = remove_surrogates(config.Messages.START_TEXT.format(
                bot_name=config.BOT_NAME,
                user_mention=callback_query.from_user.mention
            ))

            if callback_query.message.caption and callback_query.message.caption == caption:
                logger.warning(f"Start message not modified for user {callback_query.from_user.id} to avoid Telegram error.")
                return

            await callback_query.message.edit_media(
                media=InputMediaPhoto(
                    media=config.START_PHOTO,
                    caption=caption
                ),
                reply_markup=self.start_button()
            )
        except Exception as e:
            logger.error(f"Show start error for user {callback_query.from_user.id}: {str(e).encode('utf-8', 'ignore').decode('utf-8')}")

    async def show_help(self, client, callback_query: CallbackQuery):
        try:
            help_text = remove_surrogates(config.Messages.HELP_TEXT)

            if callback_query.message.text and callback_query.message.text == help_text:
                logger.warning(f"Help message not modified for user {callback_query.from_user.id} to avoid Telegram error.")
                return

            await callback_query.message.edit_text(
                help_text,
                reply_markup=self.help_button()
            )
        except Exception as e:
            logger.error(f"Show help error for user {callback_query.from_user.id}: {str(e).encode('utf-8', 'ignore').decode('utf-8')}")

    async def show_about(self, client, callback_query: CallbackQuery):
        try:
            about_text = remove_surrogates(config.Messages.ABOUT_TEXT.format(
                bot_name=config.BOT_NAME,
                version=config.BOT_VERSION
            ))

            if callback_query.message.text and callback_query.message.text == about_text:
                logger.warning(f"About message not modified for user {callback_query.from_user.id} to avoid Telegram error.")
                return

            await callback_query.message.edit_text(
                about_text,
                reply_markup=self.about_button()
            )
        except Exception as e:
            logger.error(f"Show about error for user {callback_query.from_user.id}: {str(e).encode('utf-8', 'ignore').decode('utf-8')}")

    def _channel_buttons(self) -> List[InlineKeyboardButton]:
        if config.CHANNEL_LINK and config.CHANNEL_LINK_2:
            return [
                InlineKeyboardButton("Updates 📢", url=config.CHANNEL_LINK),
                InlineKeyboardButton("Support 🆘", url=config.CHANNEL_LINK_2)
            ]
        elif config.CHANNEL_LINK:
            return [InlineKeyboardButton("Updates 📢", url=config.CHANNEL_LINK)]
        return []

    def force_sub_button(self) -> InlineKeyboardMarkup:
        buttons = []

        if config.FORCE_SUB_CHANNEL and config.CHANNEL_LINK:
            buttons.append([InlineKeyboardButton("Join Channel 🔔", url=config.CHANNEL_LINK)])
        if config.FORCE_SUB_CHANNEL_2 and config.CHANNEL_LINK_2:
            buttons.append([InlineKeyboardButton("Join Group 🔔", url=config.CHANNEL_LINK_2)])
        if config.FORCE_SUB_CHANNEL_3 and config.CHANNEL_LINK_3:
            buttons.append([InlineKeyboardButton("Join Channel 🔔", url=config.CHANNEL_LINK_3)])
        if config.FORCE_SUB_CHANNEL_4 and config.CHANNEL_LINK_4:
            buttons.append([InlineKeyboardButton("Join Channel 🔔", url=config.CHANNEL_LINK_4)])

        if config.BOT_USERNAME:
            buttons.append([
                InlineKeyboardButton("✅ Try Again", url=f"https://t.me/{config.BOT_USERNAME}?start=start")
            ])

        return InlineKeyboardMarkup(buttons)

    def start_button(self) -> InlineKeyboardMarkup:
        buttons = [
            [
                InlineKeyboardButton("Help 📜", callback_data="help"),
                InlineKeyboardButton("About ℹ️", callback_data="about")
            ]
        ]
        channel_buttons = self._channel_buttons()
        if channel_buttons:
            buttons.append(channel_buttons)

        buttons.append([InlineKeyboardButton("❄️ Owner ❄️", url=config.DEVELOPER_LINK)])
        return InlineKeyboardMarkup(buttons)

    def help_button(self) -> InlineKeyboardMarkup:
        buttons = [
            [
                InlineKeyboardButton("Home 🏠", callback_data="home"),
                InlineKeyboardButton("About ℹ️", callback_data="about")
            ]
        ]
        channel_buttons = self._channel_buttons()
        if channel_buttons:
            buttons.append(channel_buttons)

        return InlineKeyboardMarkup(buttons)

    def about_button(self) -> InlineKeyboardMarkup:
        buttons = [
            [
                InlineKeyboardButton("Home 🏠", callback_data="home"),
                InlineKeyboardButton("Help 📜", callback_data="help")
            ]
        ]
        channel_buttons = self._channel_buttons()
        if channel_buttons:
            buttons.append(channel_buttons)

        return InlineKeyboardMarkup(buttons)

    def file_button(self, file_uuid: str) -> InlineKeyboardMarkup:
        buttons = [
            [
                InlineKeyboardButton("Download 📥", callback_data=f"download_{file_uuid}"),
                InlineKeyboardButton("Share Link 🔗", callback_data=f"share_{file_uuid}")
            ]
        ]
        channel_buttons = self._channel_buttons()
        if channel_buttons:
            buttons.append(channel_buttons)

        return InlineKeyboardMarkup(buttons)

    def batch_button(self, batch_uuid: str) -> InlineKeyboardMarkup:
        buttons = [
            [
                InlineKeyboardButton("Download All 📥", callback_data=f"dlbatch_{batch_uuid}"),
                InlineKeyboardButton("Share Link 🔗", callback_data=f"share_batch_{batch_uuid}")
            ]
        ]
        channel_buttons = self._channel_buttons()
        if channel_buttons:
            buttons.append(channel_buttons)

        return InlineKeyboardMarkup(buttons)
