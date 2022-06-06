from FlameMusic import app, SUDOERS
from pyrogram import filters, Client
from pyrogram.types import Message
from FlameMusic.FlameMusicUtilities.database.onoff import (is_on_off, add_on, add_off)
from FlameMusic.FlameMusicUtilities.helpers.filters import command


@Client.on_message(command("player") & filters.user(SUDOERS))
async def smex(_, message):
    usage = "**user:**\n/player [on|off]"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    chat_id = message.chat.id
    state = message.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "on":
        user_id = 1
        await add_on(user_id)
        await message.reply_text("✅ Music Enabled for Maintenance")
    elif state == "off":
        user_id = 1
        await add_off(user_id)
        await message.reply_text("❌ Maintenance Mode Disabled")
    else:
        await message.reply_text(usage)
