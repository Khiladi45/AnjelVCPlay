import os
import time
from os import path
import random
import asyncio
import shutil
from pytube import YouTube
from yt_dlp import YoutubeDL
from FlameMusic import converter
import yt_dlp
import shutil
import psutil
from typing import Callable
from pyrogram import Client
from pyrogram.types import Message, Voice
from pytgcalls import StreamType
from pytgcalls.types.input_stream import InputAudioStream, InputStream
from sys import version as pyver
from FlameMusic import (
    dbb,
    app,
    BOT_USERNAME,
    BOT_ID,
    BOT_NAME,
    ASSID,
    ASSNAME,
    ASSUSERNAME,
    ASSMENTION,
)
from FlameMusic.FlameMusicUtilities.tgcallsrun import (
    music,
    convert,
    download,
    clear,
    get,
    is_empty,
    put,
    task_done,
    ASS_ACC,
)
from FlameMusic.FlameMusicUtilities.database.queue import (
    get_active_chats,
    is_active_chat,
    add_active_chat,
    remove_active_chat,
    music_on,
    is_music_playing,
    music_off,
)
from FlameMusic.FlameMusicUtilities.database.onoff import (
    is_on_off,
    add_on,
    add_off,
)
from FlameMusic.FlameMusicUtilities.database.chats import (
    get_served_chats,
    is_served_chat,
    add_served_chat,
    get_served_chats,
)
from FlameMusic.FlameMusicUtilities.helpers.inline import (
    play_keyboard,
    search_markup,
    play_markup,
    playlist_markup,
    audio_markup,
    play_list_keyboard,
)
from FlameMusic.FlameMusicUtilities.database.blacklistchat import (
    blacklisted_chats,
    blacklist_chat,
    whitelist_chat,
)
from FlameMusic.FlameMusicUtilities.database.gbanned import (
    get_gbans_count,
    is_gbanned_user,
    add_gban_user,
    add_gban_user,
)
from FlameMusic.FlameMusicUtilities.database.theme import (
    _get_theme,
    get_theme,
    save_theme,
)
from FlameMusic.FlameMusicUtilities.database.assistant import (
    _get_assistant,
    get_assistant,
    save_assistant,
)
from FlameMusic.config import DURATION_LIMIT
from FlameMusic.FlameMusicUtilities.helpers.decorators import authorized_users_only
from FlameMusic.FlameMusicUtilities.helpers.decorators import errors
from FlameMusic.FlameMusicUtilities.helpers.filters import command
from FlameMusic.FlameMusicUtilities.helpers.gets import (
    get_url,
    themes,
    random_assistant,
    ass_det,
)
from FlameMusic.FlameMusicUtilities.helpers.logger import LOG_CHAT
from FlameMusic.FlameMusicUtilities.helpers.thumbnails import gen_thumb
from FlameMusic.FlameMusicUtilities.helpers.chattitle import CHAT_TITLE
from FlameMusic.FlameMusicUtilities.helpers.ytdl import ytdl_opts 
from FlameMusic.FlameMusicUtilities.helpers.inline import (
    play_keyboard,
    search_markup2,
    search_markup,
)
from pyrogram import filters
from typing import Union
import subprocess
from asyncio import QueueEmpty
import shutil
import os
from youtubesearchpython import VideosSearch
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import Message, Audio, Voice
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    Message,
)

flex = {}
chat_watcher_group = 3


def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":"))))


chat_id = None
DISABLED_GROUPS = []
useer = "NaN"
que = {}



@app.on_message(
    command("music") & ~filters.edited & ~filters.bot & ~filters.private
)
@authorized_users_only
async def music_onoff(_, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    chat_title = message.chat.title
    global DISABLED_GROUPS
    try:
        user_id
    except:
        return
    if len(message.command) != 2:
        await message.reply_text("**• usage:**\n\n `/music on` & `/music off`")
        return
    status = message.text.split(None, 1)[1]
    message.chat.id
    if status in ("ON", "on", "On"):
        lel = await message.reply("`processing...`")
        if not message.chat.id in DISABLED_GROUPS:
            await lel.edit("» **FlameMusic Active.**")
            return
        DISABLED_GROUPS.remove(message.chat.id)
        await lel.edit(
            f"**✅ FlameMusic Has Been Activated In {message.chat.title}**"
        )

    elif status in ("OFF", "off", "Off"):
        lel = await message.reply("`processing...`")

        if message.chat.id in DISABLED_GROUPS:
            await lel.edit("» **FlameMusic has Disabled.**")
            return
        DISABLED_GROUPS.append(message.chat.id)
        await lel.edit(
            f"**✅ FlameMusic Has Been Disabled In {message.chat.title}**"
        )
    else:
        await message.reply_text(
            "**• user:**\n\n `/music on` & `/music off`"
        )


@Client.on_message(command(["play", f"play@{BOT_USERNAME}", "p"]))
async def play(_, message: Message):
    chat_id = message.chat.id
    if message.sender_chat:
        return await message.reply_text(
            """
You are an Anonymous Admin!
Revert back to User Account From Admin Rights.
"""
        )
    global useer
    if chat_id in DISABLED_GROUPS:
        return await message.reply_text(
            f"😕 **Sorry {message.from_user.mention}, The Flame Music is turned off by the admin**" 
        )
        return
    user_id = message.from_user.id
    chat_title = message.chat.title
    username = message.from_user.first_name
    checking = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
    if await is_on_off(1):
        LOG_ID = "-1001501090801"
        if int(chat_id) != int(LOG_ID):
            return await message.reply_text(
                f"The bot is in the process of being updated. Sorry for the inconvenience!"
            )
        return await message.reply_text(
            f"The bot is in the process of being updated. Sorry for the inconvenience!"
        )
    a = await app.get_chat_member(message.chat.id, BOT_ID)
    if a.status != "administrator":
        await message.reply_text(
            """
I ɴᴇᴇᴅ ᴛᴏ ʙᴇ ᴀɴ ᴀᴅᴍɪɴ ᴡɪᴛʜ sᴏᴍᴇ ᴘᴇʀᴍɪssɪᴏɴs:
- **ᴄᴀɴ ᴍᴀɴᴀɢᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ:** Tᴏ ᴍᴀɴᴀɢᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ
- **ᴄᴀɴ ᴅᴇʟᴇᴛᴇ ᴍᴇssᴀɢᴇs:** Tᴏ ᴅᴇʟᴇᴛᴇ Mᴜsɪᴄ Sᴇᴀʀᴄʜᴇᴅ Jᴜɴᴋ
- **ᴄᴀɴ ɪɴᴠɪᴛᴇ ᴜsᴇʀs**: Tᴏ ɪɴᴠɪᴛᴇ ᴀssɪsᴛᴀɴᴛ ᴛᴏ ᴄʜᴀᴛ
"""
        )
        return
    if not a.can_manage_voice_chats:
        await message.reply_text(
            "I ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴇ ɴᴇᴄᴇssᴀʀʏ ᴘᴇʀᴍɪssɪᴏɴs ᴛᴏ ᴘᴇʀғᴏʀᴍ ᴛʜɪs ᴀᴄᴛɪᴏɴ."
            + "\n❌ ᴍᴀɴᴀɢɪɴɢ ᴠᴏɪᴄᴇ ᴄʜᴀᴛs"
        )
        return
    if not a.can_delete_messages:
        await message.reply_text(
            "I ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴇ ɴᴇᴄᴇssᴀʀʏ ᴘᴇʀᴍɪssɪᴏɴs ᴛᴏ ᴘᴇʀғᴏʀᴍ ᴛʜɪs ᴀᴄᴛɪᴏɴ."
            + "\n❌ ᴅᴇʟᴇᴛᴇ ᴍᴇssᴀɢᴇ"
        )
        return
    if not a.can_invite_users:
        await message.reply_text(
            "I ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴇ ʀᴇϙᴜɪʀᴇᴅ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴘᴇʀғᴏʀᴍ ᴛʜɪs ᴀᴄᴛɪᴏɴ."
            + "\n❌ ɪɴᴠɪᴛᴇ ᴜsᴇʀs ᴛʜʀᴏᴜɢʜ ʟɪɴᴋ"
        )
        return
    try: 
        b = await app.get_chat_member(message.chat.id , ASSID) 
        if b.status == "banned":
            await app.unban_chat_member(message.chat.id, ASSID)
            invite_link = await app.export_chat_invite_link(message.chat.id)
            if "+" in invite_link:
                kontol = (invite_link.replace("+", "")).split("t.me/")[1]
                link_bokep = f"https://t.me/joinchat/{kontol}"
            await ASS_ACC.join_chat(link_bokep)
            await message.reply(f"{ASSNAME} Sᴜᴄᴄᴇssғᴜʟʟʏ Jᴏɪɴᴇᴅ",) 
            await remove_active_chat(chat_id)
    except UserNotParticipant:
        try:
            invite_link = await app.export_chat_invite_link(message.chat.id)
            if "+" in invite_link:
                kontol = (invite_link.replace("+", "")).split("t.me/")[1]
                link_bokep = f"https://t.me/joinchat/{kontol}"
            await ASS_ACC.join_chat(link_bokep)
            await message.reply(f"{ASSNAME} Sᴜᴄᴄᴇssғᴜʟʟʏ Jᴏɪɴeᴅ",) 
            await remove_active_chat(chat_id)
        except UserAlreadyParticipant:
            pass
        except Exception as e:
            return await message.reply_text(
                    f"""
**Assɪsᴛᴀɴᴛ Fᴀɪʟᴇᴅ ᴛᴏ Jᴏɪɴ**
**Reason**:{e}
"""
                )
    except UserAlreadyParticipant:
        pass
    except Exception as e:
        return await message.reply_text(
                    f"""
**Assɪsᴛᴀɴᴛ Fᴀɪʟᴇᴅ ᴛᴏ Jᴏɪɴ**
**Reason**:{e}
"""
            )
    audio = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    url = get_url(message)
    fucksemx = 0
    if audio:
        fucksemx = 1
        what = "Audio Searched"
        await LOG_CHAT(message, what)
        mystic = await message.reply_text(
            f"**🔄 Pʀᴏᴄᴇssɪɴɢ Aᴜᴅɪᴏ Pʀᴏᴠɪᴅᴇᴅ Bʏ {username}**"
        )
        if audio.file_size > 157286400:
            await mystic.edit_text("Aᴜᴅɪᴏ Fɪʟᴇ Sɪᴢᴇ Mᴜsᴛ Bᴇ Lᴇss Tʜᴀɴ 150 ᴍʙ")
            return
        duration = round(audio.duration / 60)
        if duration > DURATION_LIMIT:
            return await mystic.edit_text(
                f"""
**ᴅᴜʀᴀᴛɪᴏɴ ᴇʀʀᴏʀ**
**ᴀʟʟᴏᴡᴇᴅ ᴅᴜʀᴀᴛɪᴏɴ: **{DURATION_LIMIT}
**ᴀᴄᴄᴇᴘᴛᴇᴅ ᴅᴜʀᴀᴛɪᴏɴ:** {duration}
"""
            )
        file_name = (
            audio.file_unique_id
            + "."
            + (
                (audio.file_name.split(".")[-1])
                if (not isinstance(audio, Voice))
                else "ogg"
            )
        )
        file_name = path.join(path.realpath("downloads"), file_name)
        file = await convert(
            (await message.reply_to_message.download(file_name))
            if (not path.isfile(file_name))
            else file_name,
        )
        title = "sᴇʟᴇᴄᴛᴇᴅ ᴀᴜᴅɪᴏ ғʀᴏᴍ ᴛᴇʟᴇɢʀᴀᴍ"
        link = "https://t.me/Flame_project"
        thumb = "cache/Audio.png"
        videoid = "smex1"
    elif url:
        what = "URL Searched"
        await LOG_CHAT(message, what)
        query = message.text.split(None, 1)[1]
        mystic = await message.reply_text("Processing Url")
        ydl_opts = {"format": "bestaudio/best"}
        try:
            results = VideosSearch(query, limit=1)
            for result in results.result()["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"]
                link = result["link"]
                (result["id"])
                videoid = result["id"]
        except Exception as e:
            return await mystic.edit_text(
                f"sᴏɴɢ ɴᴏᴛ ғᴏᴜɴᴅ.\n**ᴘᴏssɪʙʟᴇ ʀᴇᴀsᴏɴ:** {e}"
            )
        smex = int(time_to_seconds(duration))
        if smex > DURATION_LIMIT:
            return await mystic.edit_text(
                f"""
**ᴅᴜʀᴀᴛɪᴏɴ ᴇʀʀᴏʀ**
**ᴀʟʟᴏᴡᴇᴅ ᴅᴜʀᴀᴛɪᴏɴ:** {DURATION_LIMIT}
**ᴀᴄᴄᴇᴘᴛᴇᴅ ᴅᴜʀᴀᴛɪon:** {duration}
"""
            )
        if duration == "None":
            return await mystic.edit_text("sᴏʀʀʏ! ʟɪᴠᴇ ᴠɪᴅᴇᴏ ɪs ɴᴏᴛ sᴜᴘᴘᴏʀᴛᴇᴅ")
        if views == "None":
            return await mystic.edit_text("sᴏʀʀʏ! ʟɪᴠᴇ ᴠɪᴅᴇᴏ ɪs ɴᴏᴛ sᴜᴘᴘᴏʀᴛᴇᴅ")
        semxbabes = f"Downloading {title[:50]}"
        await mystic.edit(semxbabes)
        theme = random.choice(themes)
        ctitle = message.chat.title
        ctitle = await CHAT_TITLE(ctitle)
        userid = message.from_user.id
        thumb = await gen_thumb(thumbnail, title, userid, theme, ctitle)

        def my_hook(d):
            if d["status"] == "downloading":
                percentage = d["_percent_str"]
                per = (str(percentage)).replace(".", "", 1).replace("%", "", 1)
                per = int(per)
                eta = d["eta"]
                speed = d["_speed_str"]
                size = d["_total_bytes_str"]
                bytesx = d["total_bytes"]
                if str(bytesx) in flex:
                    pass
                else:
                    flex[str(bytesx)] = 1
                if flex[str(bytesx)] == 1:
                    flex[str(bytesx)] += 1
                    try:
                        if eta > 2:
                            mystic.edit(
                                f"Downloading {title[:50]}\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec"
                            )
                    except Exception:
                        pass
                if per > 250:
                    if flex[str(bytesx)] == 2:
                        flex[str(bytesx)] += 1
                        if eta > 2:
                            mystic.edit(
                                f"Downloading {title[:50]}..\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec"
                            )
                        print(
                            f"[{videoid}] Downloaded {percentage} at a speed of {speed} | ETA: {eta} seconds"
                        )
                if per > 500:
                    if flex[str(bytesx)] == 3:
                        flex[str(bytesx)] += 1
                        if eta > 2:
                            mystic.edit(
                                f"Downloading {title[:50]}...\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec"
                            )
                        print(
                            f"[{videoid}] Downloaded {percentage} at a speed of {speed} | ETA: {eta} seconds"
                        )
                if per > 800:
                    if flex[str(bytesx)] == 4:
                        flex[str(bytesx)] += 1
                        if eta > 2:
                            mystic.edit(
                                f"Downloading {title[:50]}....\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec"
                            )
                        print(
                            f"[{videoid}] Downloaded {percentage} at a speed of {speed} | ETA: {eta} seconds"
                        )
            if d["status"] == "finished":
                try:
                    taken = d["_elapsed_str"]
                except Exception:
                    taken = "00:00"
                size = d["_total_bytes_str"]
                mystic.edit(
                    f"**Downloaded {title[:50]}.....**\n\n**FileSize:** {size}\n**Time Taken:** {taken} sec\n\n**Converting File**[__FFmpeg processing__]"
                )
                print(f"[{videoid}] Downloaded| Elapsed: {taken} seconds")

        loop = asyncio.get_event_loop()
        x = await loop.run_in_executor(None, download, link, my_hook)
        file = await convert(x)
    else:
        if len(message.command) < 2:
            what = "Command"
            await LOG_CHAT(message, what)
            user_name = message.from_user.first_name
            thumb ="cache/IMG_20211230_165039_159.jpg"
            buttons = playlist_markup(user_name, user_id)
            hmo = await message.reply_photo(
            photo=thumb, 
            caption=("**User:** /play [ᴍᴜsɪᴄ ɴᴀᴍᴇ ᴏʀ ʏᴏᴜᴛᴜʙᴇ ʟɪɴᴋ ᴏʀ ʀᴇᴘʟʏ ᴀᴜᴅɪo]\n\ɪғ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴄʀᴇᴀᴛᴇ ᴀ ᴘʟᴀʏʟɪsᴛ! ᴄʜᴏᴏsᴇ ᴛʜᴇ ᴏɴᴇ ғʀᴏᴍ ʙᴇʟᴏᴡ."),    
            reply_markup=InlineKeyboardMarkup(buttons),
            )
            return
        what = "Query Given"
        await LOG_CHAT(message, what)
        query = message.text.split(None, 1)[1]
        mystic = await message.reply_text("**🔎 sᴇᴀʀᴄʜ**")
        try:
            a = VideosSearch(query, limit=5)
            result = (a.result()).get("result")
            title1 = result[0]["title"]
            duration1 = result[0]["duration"]
            title2 = result[1]["title"]
            duration2 = result[1]["duration"]
            title3 = result[2]["title"]
            duration3 = result[2]["duration"]
            title4 = result[3]["title"]
            duration4 = result[3]["duration"]
            title5 = result[4]["title"]
            duration5 = result[4]["duration"]
            ID1 = result[0]["id"]
            ID2 = result[1]["id"]
            ID3 = result[2]["id"]
            ID4 = result[3]["id"]
            ID5 = result[4]["id"]
        except Exception as e:
            return await mystic.edit_text(
                f"Lagu Tidak Ditemukan.\n**Kemungkinan Alasan:** {e}"
            )
        thumb ="cache/IMG_20211230_211518_897.jpg"
        await mystic.delete()
        buttons = search_markup(ID1, ID2, ID3, ID4, ID5, duration1, duration2, duration3, duration4, duration5, user_id, query)
        hmo = await message.reply_photo(
            photo=thumb,
            caption=f"**✨ ᴘʟᴇᴀsᴇ sᴇʟᴇᴄᴛ ᴛʜᴇ sᴏɴɢ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴘʟᴀʏ**\n\n¹ <b>{title1}</b>\n  ┗ 💡 <u>__[More Information](https://t.me/{BOT_USERNAME}?start=info_{ID1})__</u>\n  ┗ ⚡ __Powered by {BOT_NAME}__\n\n² <b>{title2}</b>\n  ┗ 💡 <u>__[More Information](https://t.me/{BOT_USERNAME}?start=info_{ID2})__</u>\n  ┗ ⚡ __Powered by {BOT_NAME}__\n\n³ <b>{title3}</b>\n  ┗ 💡 <u>__[More Information](https://t.me/{BOT_USERNAME}?start=info_{ID3})__</u>\n  ┗ ⚡ __Powered by {BOT_NAME}__\n\n⁴ <b>{title4}</b>\n  ┗ 💡 <u>__[More Information](https://t.me/{BOT_USERNAME}?start=info_{ID4})__</u>\n  ┗ ⚡ __Powered by {BOT_NAME}__\n\n⁵ <b>{title5}</b>\n  ┗ 💡 <u>__[More Information](https://t.me/{BOT_USERNAME}?start=info_{ID5})__</u>\n  ┗ ⚡ __Powered by {BOT_NAME}__",    
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        disable_web_page_preview=False
        return
    if await is_active_chat(chat_id):
        position = await put(chat_id, file=file)
        _chat_ = (str(file)).replace("_", "", 1).replace("/", "", 1).replace(".", "", 1)
        cpl = f"downloads/{_chat_}final.png"
        shutil.copyfile(thumb, cpl)
        f20 = open(f"search/{_chat_}title.txt", "w")
        f20.write(f"{title}")
        f20.close()
        f111 = open(f"search/{_chat_}duration.txt", "w")
        f111.write(f"{duration}")
        f111.close()
        f27 = open(f"search/{_chat_}username.txt", "w")
        f27.write(f"{checking}")
        f27.close()
        if fucksemx != 1:
            f28 = open(f"search/{_chat_}videoid.txt", "w")
            f28.write(f"{videoid}")
            f28.close()
            buttons = play_markup(videoid, user_id)
        else:
            f28 = open(f"search/{_chat_}videoid.txt", "w")
            f28.write(f"{videoid}")
            f28.close()
            buttons = audio_markup(videoid, user_id)
        checking = (
            f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
        )
        await message.reply_photo(
            photo=thumb,
            caption=f"""
<b>💡 ᴛʀᴀᴄᴋs ᴀᴅᴅᴇᴅ ᴛᴏ ϙᴜᴇᴜᴇ</b>
<b>🏷🇳ᴀᴍᴇ: [{title[:25]}]({link})</b>
<b>⏱️ 🇩ᴜʀᴀᴛɪᴏɴ:</b> {duration} \n
<b>🎧 🇷ᴇϙᴜᴇsᴛᴇᴅ ʙʏ: </b>{checking}
<b>🇶ᴜᴇᴜᴇ ᴘᴏsɪᴛɪᴏɴ</b> {position}
<b>ɢᴏᴅғᴀᴛʜᴇʀ ᴏғ ᴛʜɪs ʙᴏᴛ @xmartperson</b>
""",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        return await mystic.delete()
    else:
        await music_on(chat_id)
        await add_active_chat(chat_id)
        await music.pytgcalls.join_group_call(
            chat_id,
            InputStream(
                InputAudioStream(
                    file,
                ),
            ),
            stream_type=StreamType().local_stream,
        )
        _chat_ = (str(file)).replace("_", "", 1).replace("/", "", 1).replace(".", "", 1)
        checking = (
            f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
        )
        if fucksemx != 1:
            f28 = open(f"search/{_chat_}videoid.txt", "w")
            f28.write(f"{videoid}")
            f28.close()
            buttons = play_markup(videoid, user_id)
        else:
            f28 = open(f"search/{_chat_}videoid.txt", "w")
            f28.write(f"{videoid}")
            f28.close()
            buttons = audio_markup(videoid, user_id)
        await message.reply_photo(
            photo=thumb,
            reply_markup=InlineKeyboardMarkup(buttons),
            caption=f"""
<b>🏷 🇳ᴀᴍᴇ:</b> [{title[:25]}]({link})
<b>⏱️ 🇩ᴜʀᴀᴛɪᴏɴ:</b> {duration}
<b>🎧 🇷ᴇϙᴜᴇsᴛᴇᴅ ʙʏ:</b> {checking}
""",
        )
        return await mystic.delete()


@Client.on_callback_query(filters.regex(pattern=r"FlameMusic"))
async def startyuplay(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    chat_id = CallbackQuery.message.chat.id
    CallbackQuery.message.chat.title
    callback_request = callback_data.split(None, 1)[1]
    userid = CallbackQuery.from_user.id
    try:
        id, duration, user_id = callback_request.split("|")
    except Exception as e:
        return await CallbackQuery.message.edit(
            f"Error Occured\n**Possible reason could be**:{e}"
        )
    if duration == "None":
        return await CallbackQuery.message.reply_text(
            f"Sorry!, Live Videos are not supported"
        )
    if CallbackQuery.from_user.id != int(user_id):
        return await CallbackQuery.answer(
            "This is not for you! Search You Own Song nigga", show_alert=True
        )
    await CallbackQuery.message.delete()
    checking = f"[{CallbackQuery.from_user.first_name}](tg://user?id={userid})"
    url = f"https://www.youtube.com/watch?v={id}"
    videoid = id
    smex = int(time_to_seconds(duration))
    if smex > DURATION_LIMIT:
        await CallbackQuery.message.reply_text(
            f"""
**ᴅᴜʀᴀᴛɪᴏɴ ᴇʀʀᴏʀ**
**ᴀʟʟᴏᴡᴇᴅ ᴅᴜʀᴀᴛɪᴏɴ: {DURATION_LIMIT}**
**ᴀᴄᴄᴇᴘᴛᴇᴅ ᴅᴜʀᴀᴛɪᴏɴ:** {duration}
"""
        )
        return
    try:
        with yt_dlp.YoutubeDL(ytdl_opts) as ytdl:
            x = ytdl.extract_info(url, download=False)
    except Exception as e:
        return await CallbackQuery.message.reply_text(
            f"ғᴀɪʟᴇᴅ ᴛᴏ ʟᴏᴀᴅ ᴠɪᴅᴇᴏ..\n\n**ʀᴇᴀsᴏɴ**: {e}"
        )
    title = x["title"]
    mystic = await CallbackQuery.message.reply_text(f"Downloading {title[:50]}")
    thumbnail = x["thumbnail"]
    (x["id"])
    videoid = x["id"]

    def my_hook(d):
        if d["status"] == "downloading":
            percentage = d["_percent_str"]
            per = (str(percentage)).replace(".", "", 1).replace("%", "", 1)
            per = int(per)
            eta = d["eta"]
            speed = d["_speed_str"]
            size = d["_total_bytes_str"]
            bytesx = d["total_bytes"]
            if str(bytesx) in flex:
                pass
            else:
                flex[str(bytesx)] = 1
            if flex[str(bytesx)] == 1:
                flex[str(bytesx)] += 1
                try:
                    if eta > 2:
                        mystic.edit(
                            f"Downloading {title[:50]}\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec"
                        )
                except Exception:
                    pass
            if per > 250:
                if flex[str(bytesx)] == 2:
                    flex[str(bytesx)] += 1
                    if eta > 2:
                        mystic.edit(
                            f"Downloading {title[:50]}..\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec"
                        )
                    print(
                        f"[{videoid}] Downloaded {percentage} at a speed of {speed} | ETA: {eta} seconds"
                    )
            if per > 500:
                if flex[str(bytesx)] == 3:
                    flex[str(bytesx)] += 1
                    if eta > 2:
                        mystic.edit(
                            f"Downloading {title[:50]}...\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec"
                        )
                    print(
                        f"[{videoid}] Downloaded {percentage} at a speed of {speed} | ETA: {eta} seconds"
                    )
            if per > 800:
                if flex[str(bytesx)] == 4:
                    flex[str(bytesx)] += 1
                    if eta > 2:
                        mystic.edit(
                            f"Downloading {title[:50]}....\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec"
                        )
                    print(
                        f"[{videoid}] Downloaded {percentage} at a speed of {speed} | ETA: {eta} seconds"
                    )
        if d["status"] == "finished":
            try:
                taken = d["_elapsed_str"]
            except Exception:
                taken = "00:00"
            size = d["_total_bytes_str"]
            mystic.edit(
                f"**Downloaded {title[:50]}.....**\n\n**FileSize:** {size}\n**Time Taken:** {taken} sec\n\n**Converting File**[__FFmpeg processing__]"
            )
            print(f"[{videoid}] Downloaded| Elapsed: {taken} seconds")

    loop = asyncio.get_event_loop()
    x = await loop.run_in_executor(None, download, url, my_hook)
    file = await convert(x)
    theme = random.choice(themes)
    ctitle = CallbackQuery.message.chat.title
    ctitle = await CHAT_TITLE(ctitle)
    thumb = await gen_thumb(thumbnail, title, userid, theme, ctitle)
    await mystic.delete()
    if await is_active_chat(chat_id):
        position = await put(chat_id, file=file)
        buttons = play_markup(videoid, user_id)
        _chat_ = (str(file)).replace("_", "", 1).replace("/", "", 1).replace(".", "", 1)
        cpl = f"downloads/{_chat_}final.png"
        shutil.copyfile(thumb, cpl)
        f20 = open(f"search/{_chat_}title.txt", "w")
        f20.write(f"{title}")
        f20.close()
        f111 = open(f"search/{_chat_}duration.txt", "w")
        f111.write(f"{duration}")
        f111.close()
        f27 = open(f"search/{_chat_}username.txt", "w")
        f27.write(f"{checking}")
        f27.close()
        f28 = open(f"search/{_chat_}videoid.txt", "w")
        f28.write(f"{videoid}")
        f28.close()
        await mystic.delete()
        m = await CallbackQuery.message.reply_photo(
            photo=thumb,
            caption=f"""
<b>💡 ᴛʀᴀᴄᴋs ᴀᴅᴅᴇᴅ ᴛᴏ ϙᴜᴇᴜᴇ</b>
<b>🏷 🇳ᴀᴍᴇ:</b>[{title[:25]}]({url})
<b>⏱️ 🇩ᴜʀᴀᴛɪᴏɴ:</b> {duration}
<b>💡</b> [More Information](https://t.me/{BOT_USERNAME}?start=info_{id})
<b>🎧 🇷:</b> {checking}
<b>🇶ᴜᴇᴜᴇ ᴘᴏsɪᴛɪᴏɴ</b> {position}
""",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        os.remove(thumb)
        await CallbackQuery.message.delete()
    else:
        await music_on(chat_id)
        await add_active_chat(chat_id)
        await music.pytgcalls.join_group_call(
            chat_id,
            InputStream(
                InputAudioStream(
                    file,
                ),
            ),
            stream_type=StreamType().local_stream,
        )
        buttons = play_markup(videoid, user_id)
        await mystic.delete()
        m = await CallbackQuery.message.reply_photo(
            photo=thumb,
            reply_markup=InlineKeyboardMarkup(buttons),
            caption=f"""
<b>🏷 🇳ᴀᴍᴇ:</b> [{title[:25]}]({url})
<b>⏱️ 🇩ᴜʀᴀᴛɪᴏɴ:</b> {duration}
<b>💡</b> [More Information](https://t.me/{BOT_USERNAME}?start=info_{id})
<b>🎧 🇷ᴇϙᴜᴇsᴛᴇᴅ ʙʏ:</b> {checking}
""",
        )
        os.remove(thumb)
        await CallbackQuery.message.delete()


@Client.on_callback_query(filters.regex(pattern=r"popat"))
async def popat(_,CallbackQuery): 
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    print(callback_request)
    userid = CallbackQuery.from_user.id 
    try:
        id , query, user_id = callback_request.split("|") 
    except Exception as e:
        return await CallbackQuery.message.edit(f"ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀs\n**ᴛʜᴇ ᴘᴏssɪʙʟᴇ ʀᴇᴀsᴏɴs ᴀʀᴇ**:{e}")       
    if CallbackQuery.from_user.id != int(user_id):
        return await CallbackQuery.answer("This is not for you! Search You Own Song", show_alert=True)
    i=int(id)
    query = str(query)
    try:
        a = VideosSearch(query, limit=10)
        result = (a.result()).get("result")
        title1 = (result[0]["title"])
        duration1 = (result[0]["duration"])
        title2 = (result[1]["title"])
        duration2 = (result[1]["duration"])      
        title3 = (result[2]["title"])
        duration3 = (result[2]["duration"])
        title4 = (result[3]["title"])
        duration4 = (result[3]["duration"])
        title5 = (result[4]["title"])
        duration5 = (result[4]["duration"])
        title6 = (result[5]["title"])
        duration6 = (result[5]["duration"])
        title7= (result[6]["title"])
        duration7 = (result[6]["duration"])      
        title8 = (result[7]["title"])
        duration8 = (result[7]["duration"])
        title9 = (result[8]["title"])
        duration9 = (result[8]["duration"])
        title10 = (result[9]["title"])
        duration10 = (result[9]["duration"])
        ID1 = (result[0]["id"])
        ID2 = (result[1]["id"])
        ID3 = (result[2]["id"])
        ID4 = (result[3]["id"])
        ID5 = (result[4]["id"])
        ID6 = (result[5]["id"])
        ID7 = (result[6]["id"])
        ID8 = (result[7]["id"])
        ID9 = (result[8]["id"])
        ID10 = (result[9]["id"])                    
    except Exception as e:
        return await mystic.edit_text(f"sᴏɴɢ ɴᴏᴛ ғᴏᴜɴᴅ\n**ᴘᴏssɪʙʟᴇ ʀᴇᴀsᴏɴ:**{e}")
    if i == 1:
        buttons = search_markup2(ID6, ID7, ID8, ID9, ID10, duration6, duration7, duration8, duration9, duration10 ,user_id, query)
        await CallbackQuery.edit_message_text(
            f"**✨ ᴘʟᴇᴀsᴇ sᴇʟᴇᴄᴛ ᴛʜᴇ sᴏɴɢ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴘʟᴀʏ**\n\n⁶ <b>{title6}</b>\n  ┗ 💡 <u>__[More Information](https://t.me/{BOT_USERNAME}?start=info_{ID6})__</u>\n  ┗ ⚡ __Powered by {BOT_NAME}__\n\n⁷ <b>{title7}</b>\n  ┗ 💡 <u>__[More Information](https://t.me/{BOT_USERNAME}?start=info_{ID7})__</u>\n  ┗ ⚡ __Powered by {BOT_NAME}__\n\n⁸ <b>{title8}</b>\n  ┗ 💡 <u>__[More Information](https://t.me/{BOT_USERNAME}?start=info_{ID8})__</u>\n  ┗ ⚡ __Powered by {BOT_NAME}__\n\n⁹ <b>{title9}</b>\n  ┗ 💡 <u>__[More Information](https://t.me/{BOT_USERNAME}?start=info_{ID9})__</u>\n  ┗ ⚡ __Powered by {BOT_NAME}__\n\n¹⁰ <b>{title10}</b>\n  ┗ 💡 <u>__[More Information](https://t.me/{BOT_USERNAME}?start=info_{ID10})__</u>\n  ┗ ⚡ __Powered by {BOT_NAME}__",    
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=False
        )  
        return    
    if i == 2:
        buttons = search_markup(ID1, ID2, ID3, ID4, ID5, duration1, duration2, duration3, duration4, duration5, user_id, query)
        await CallbackQuery.edit_message_text(
            f"**✨ ᴘʟᴇᴀsᴇ sᴇʟᴇᴄᴛ ᴛʜᴇ sᴏɴɢ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴘʟᴀʏ**\n\n¹ <b>{title1}</b>\n  ┗ 💡 <u>__[More Information](https://t.me/{BOT_USERNAME}?start=info_{ID1})__</u>\n  ┗ ⚡ __Powered by {BOT_NAME}__\n\n² <b>{title2}</b>\n  ┗ 💡 <u>__[More Information](https://t.me/{BOT_USERNAME}?start=info_{ID2})__</u>\n  ┗ ⚡ __Powered by {BOT_NAME}__\n\n³ <b>{title3}</b>\n  ┗ 💡 <u>__[More Information](https://t.me/{BOT_USERNAME}?start=info_{ID3})__</u>\n  ┗ ⚡ __Powered by {BOT_NAME}__\n\n⁴ <b>{title4}</b>\n  ┗ 💡 <u>__[More Information](https://t.me/{BOT_USERNAME}?start=info_{ID4})__</u>\n  ┗ ⚡ __Powered by {BOT_NAME}__\n\n⁵ <b>{title5}</b>\n  ┗ 💡 <u>__[More Information](https://t.me/{BOT_USERNAME}?start=info_{ID5})__</u>\n  ┗ ⚡ __Powered by {BOT_NAME}__",    
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=False 
        )  
        return
            


@app.on_message(filters.command("playplaylist"))
async def play_playlist_cmd(_, message):
    thumb ="cache/IMG_20211230_211509_034.jpg"
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    buttons = playlist_markup(user_name, user_id)
    await message.reply_photo(
    photo=thumb, 
    caption=("**__AnjelMusic's Playlist Feature__**\n\nSelect the Playlist you want to play!."),    
    reply_markup=InlineKeyboardMarkup(buttons),
    )
    return
