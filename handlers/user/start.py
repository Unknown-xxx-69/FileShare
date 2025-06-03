from pyrogram import Client, filters
from pyrogram.types import Message
from database import Database
from utils import ButtonManager
from .utils.message_delete import schedule_message_deletion
import config
import asyncio
import logging
import base64

logger = logging.getLogger(__name__)
db = Database()
button_manager = ButtonManager()

async def decode_codex_link(encoded_string: str) -> tuple:
    try:
        padding_needed = len(encoded_string) % 4
        if padding_needed:
            encoded_string += '=' * (4 - padding_needed)
        string_bytes = base64.b64decode(encoded_string.encode("ascii"))
        decoded = string_bytes.decode("ascii")

        if decoded.startswith("get-"):
            parts = decoded.split("-")
            if len(parts) == 2:
                msg_id = int(parts[1]) // abs(config.DB_CHANNEL_ID)
                return False, [msg_id]
            elif len(parts) == 3:
                first_id = int(parts[1]) // abs(config.DB_CHANNEL_ID)
                last_id = int(parts[2]) // abs(config.DB_CHANNEL_ID)
                return True, list(range(first_id, last_id + 1))
        return False, []
    except Exception as e:
        logger.error(f"Error decoding CodeXBotz link: {str(e)}")
        return False, []

async def send_auto_delete_info(client, chat_id, msg_ids: list):
    delete_time = config.AUTO_DELETE_TIME
    info_msg = await client.send_message(
        chat_id=chat_id,
        text=f"⏳ **Auto Delete Information**\n\n"
             f"➜ This file will be deleted in {delete_time} minutes.\n"
             f"➜ Forward this file to your saved messages or another chat to save it permanently.",
        protect_content=config.PRIVACY_MODE
    )
    if info_msg and info_msg.id:
        msg_ids.append(info_msg.id)
        asyncio.create_task(schedule_message_deletion(client, chat_id, msg_ids, delete_time))

@Client.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    try:
        await db.add_user(message.from_user.id, message.from_user.mention)
    except Exception as e:
        logger.error(f"Error adding user to database: {str(e)}")

    user_mention = message.from_user.mention

    if len(message.command) > 1:
        command = message.command[1]

        force_sub_status = await button_manager.check_force_sub(client, message.from_user.id)
        if not force_sub_status:
            force_sub_text = "**⚠️ You must join our channel(s) to use this bot!**\n\n"
            channels = [
                (config.FORCE_SUB_CHANNEL, "Join Channel 1"),
                (config.FORCE_SUB_CHANNEL_2, "Join Channel 2"),
                (config.FORCE_SUB_CHANNEL_3, "Join Channel 3"),
                (config.FORCE_SUB_CHANNEL_4, "Join Channel 4")
            ]
            for ch_id, name in channels:
                if ch_id != 0:
                    force_sub_text += f"• {name}\n"
            force_sub_text += "\nJoin and try again."

            await message.reply_text(
                force_sub_text,
                reply_markup=button_manager.force_sub_button(),
                protect_content=config.PRIVACY_MODE
            )
            return

        is_codex_batch, message_ids = await decode_codex_link(command)

        if message_ids:
            if is_codex_batch:
                status_msg = await message.reply_text(
                    f"🔄 **Processing Batch Download**\n\n"
                    f"📦 Total Files: {len(message_ids)}\n"
                    f"⏳ Please wait...",
                    protect_content=config.PRIVACY_MODE
                )
                success, fail, sent_msgs = 0, 0, []

                for msg_id in message_ids:
                    try:
                        msg = await client.copy_message(
                            chat_id=message.chat.id,
                            from_chat_id=config.DB_CHANNEL_ID,
                            message_id=msg_id,
                            protect_content=config.PRIVACY_MODE
                        )
                        if msg:
                            sent_msgs.append(msg.id)
                            success += 1
                    except Exception as e:
                        fail += 1
                        logger.error(f"Batch file send error: {str(e)}")

                if success > 0 and config.AUTO_DELETE_TIME:
                    await send_auto_delete_info(client, message.chat.id, sent_msgs)

                await status_msg.edit_text(
                    f"✅ **Batch Download Complete**\n\n"
                    f"📥 Sent: {success}\n❌ Failed: {fail}"
                )
                return
            else:
                try:
                    msg = await client.copy_message(
                        chat_id=message.chat.id,
                        from_chat_id=config.DB_CHANNEL_ID,
                        message_id=message_ids[0],
                        protect_content=config.PRIVACY_MODE
                    )
                    if msg and config.AUTO_DELETE_TIME:
                        await send_auto_delete_info(client, message.chat.id, [msg.id])
                    return
                except Exception:
                    await message.reply_text("❌ File not found or has been deleted!", protect_content=config.PRIVACY_MODE)
                    return

        if command.startswith("batch_"):
            batch_uuid = command.replace("batch_", "")
            batch_data = await db.get_batch(batch_uuid)

            if not batch_data:
                await message.reply_text("❌ Batch not found or has been deleted!", protect_content=config.PRIVACY_MODE)
                return

            status_msg = await message.reply_text(
                f"🔄 **Processing Batch Download**\n\n"
                f"📦 Total Files: {len(batch_data['files'])}\n"
                f"⏳ Please wait...",
                protect_content=config.PRIVACY_MODE
            )

            success, fail, sent_msgs = 0, 0, []
            for file_uuid in batch_data["files"]:
                file_data = await db.get_file(file_uuid)
                if file_data and "message_id" in file_data:
                    try:
                        msg = await client.copy_message(
                            chat_id=message.chat.id,
                            from_chat_id=config.DB_CHANNEL_ID,
                            message_id=file_data["message_id"],
                            protect_content=config.PRIVACY_MODE
                        )
                        if msg:
                            sent_msgs.append(msg.id)
                            success += 1
                    except Exception as e:
                        fail += 1
                        logger.error(f"Batch file send error: {str(e)}")

            if success > 0 and config.AUTO_DELETE_TIME:
                await send_auto_delete_info(client, message.chat.id, sent_msgs)

            if success > 0:
                await db.increment_batch_downloads(batch_uuid)

            await status_msg.edit_text(
                f"✅ **Batch Download Complete**\n\n"
                f"📥 Sent: {success}\n❌ Failed: {fail}"
            )
            return

        # Fallback: handle single file by UUID
        file_data = await db.get_file(command)
        if file_data:
            try:
                msg = await client.copy_message(
                    chat_id=message.chat.id,
                    from_chat_id=config.DB_CHANNEL_ID,
                    message_id=file_data["message_id"],
                    protect_content=config.PRIVACY_MODE
                )
                if msg:
                    await db.increment_downloads(command)
                    if config.AUTO_DELETE_TIME:
                        await send_auto_delete_info(client, message.chat.id, [msg.id])
            except Exception as e:
                await message.reply_text(f"❌ Error: {str(e)}", protect_content=config.PRIVACY_MODE)
        else:
            await message.reply_text("❌ Invalid or expired link.", protect_content=config.PRIVACY_MODE)

    else:
        buttons = button_manager.start_button()
        await message.reply_photo(
            photo=config.START_PHOTO,
            caption=config.Messages.START_TEXT.format(bot_name=config.BOT_NAME, user_mention=user_mention),
            reply_markup=buttons
        )
