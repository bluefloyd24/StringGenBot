import asyncio

from pyrogram import Client, filters
from oldpyro import Client as Client1
from oldpyro.errors import ApiIdInvalid as ApiIdInvalid1
from oldpyro.errors import PasswordHashInvalid as PasswordHashInvalid1
from oldpyro.errors import PhoneCodeExpired as PhoneCodeExpired1
from oldpyro.errors import PhoneCodeInvalid as PhoneCodeInvalid1
from oldpyro.errors import PhoneNumberInvalid as PhoneNumberInvalid1
from oldpyro.errors import SessionPasswordNeeded as SessionPasswordNeeded1
from pyrogram.errors import (
    ApiIdInvalid,
    FloodWait,
    PasswordHashInvalid,
    PhoneCodeExpired,
    PhoneCodeInvalid,
    PhoneNumberInvalid,
    SessionPasswordNeeded,
)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from telethon import TelegramClient
from telethon.errors import (
    ApiIdInvalidError,
    PasswordHashInvalidError,
    PhoneCodeExpiredError,
    PhoneCodeInvalidError,
    PhoneNumberInvalidError,
    SessionPasswordNeededError,
)
from telethon.sessions import StringSession
from telethon.tl.functions.channels import JoinChannelRequest
from pyromod.listen.listen import ListenerTimeout

from config import SUPPORT_CHAT
from StringGen import Anony
from StringGen.utils import retry_key


async def gen_session(
    message, user_id: int, telethon: bool = False, old_pyro: bool = False
):
    if telethon:
        ty = f"Telethon"
    elif old_pyro:
        ty = f"Pyrogram ver1"
    else:
        ty = f"Pyrogram ver2"

    await message.reply_text(f"×.. Trying to connnet {ty} generator...")

    try:
        api_id = await Anony.ask(
            identifier=(message.chat.id, user_id, None),
            text="👇 Send your API_ID ;",
            filters=filters.text,
            timeout=300,
        )
    except ListenerTimeout:
        return await Anony.send_message(
            user_id,
            "🙅TIMEOUT! Please start generating again...",
            reply_markup=retry_key,
        )

    if await cancelled(api_id):
        return

    try:
        api_id = int(api_id.text)
    except ValueError:
        return await Anony.send_message(
            user_id,
            "🚫 INVALID API ID! Please start generating again...",
            reply_markup=retry_key,
        )

    try:
        api_hash = await Anony.ask(
            identifier=(message.chat.id, user_id, None),
            text="👇 Send your API_HASH ;",
            filters=filters.text,
            timeout=300,
        )
    except ListenerTimeout:
        return await Anony.send_message(
            user_id,
            "🙅TIMEOUT! Please start generating again...",
            reply_markup=retry_key,
        )

    if await cancelled(api_hash):
        return

    api_hash = api_hash.text

    if len(api_hash) < 30:
        return await Anony.send_message(
            user_id,
            "🚫 INVALID API HASH! Please start generating again...",
            reply_markup=retry_key,
        )

    try:
        phone_number = await Anony.ask(
            identifier=(message.chat.id, user_id, None),
            text="👇 Send your PHONE_NUMBERS ;",
            filters=filters.text,
            timeout=300,
        )
    except ListenerTimeout:
        return await Anony.send_message(
            user_id,
            "🙅TIMEOUT! Please start generating again...",
            reply_markup=retry_key,
        )

    if await cancelled(phone_number):
        return
    phone_number = phone_number.text

    await Anony.send_message(user_id, "×.. Trying to send OTP to your account...")
    if telethon:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif old_pyro:
        client = Client1(":memory:", api_id=api_id, api_hash=api_hash)
    else:
        client = Client(name="Anony", api_id=api_id, api_hash=api_hash, in_memory=True)
    await client.connect()

    try:
        if telethon:
            code = await client.send_code_request(phone_number)
        else:
            code = await client.send_code(phone_number)
        await asyncio.sleep(1)

    except FloodWait as f:
        return await Anony.send_message(
            user_id,
            f"Failed to send code to login. \n\Please for {f.value or f.x} Second and try again.",
            reply_markup=retry_key,
        )
    except (ApiIdInvalid, ApiIdInvalidError, ApiIdInvalid1):
        return await Anony.send_message(
            user_id,
            "🚫 INVALID API ID/HASH! Please start generating again...",
            reply_markup=retry_key,
        )
    except (PhoneNumberInvalid, PhoneNumberInvalidError, PhoneNumberInvalid1):
        return await Anony.send_message(
            user_id,
            "🚫 INVALID PHONE NUMBER! Please start generating again...",
            reply_markup=retry_key,
        )

    try:
        otp = await Anony.ask(
            identifier=(message.chat.id, user_id, None),
            text=f"✅ OTP is on {phone_number}.\nIf the otp is<code>12345</code>, Please send it as <code>1 2 3 4 5.</code>",
            filters=filters.text,
            timeout=600,
        )
        if await cancelled(otp):
            return
    except ListenerTimeout:
        return await Anony.send_message(
            user_id,
            "🙅TIMEOUT! Please start generating again...",
            reply_markup=retry_key,
        )

    otp = otp.text.replace(" ", "")
    try:
        if telethon:
            await client.sign_in(phone_number, otp, password=None)
        else:
            await client.sign_in(phone_number, code.phone_code_hash, otp)
    except (PhoneCodeInvalid, PhoneCodeInvalidError, PhoneCodeInvalid1):
        return await Anony.send_message(
            user_id,
            "🚫 ERROR CODE! Please start generating again...",
            reply_markup=retry_key,
        )
    except (PhoneCodeExpired, PhoneCodeExpiredError, PhoneCodeExpired1):
        return await Anony.send_message(
            user_id,
            "🚫 EXPIRED CODE, USE SPACE BETWEEN THE CODE!\nPlease start generating again...",
            reply_markup=retry_key,
        )
    except (SessionPasswordNeeded, SessionPasswordNeededError, SessionPasswordNeeded1):
        try:
            pwd = await Anony.ask(
                identifier=(message.chat.id, user_id, None),
                text=" 👇 Send your PASSWORD ;",
                filters=filters.text,
                timeout=300,
            )
        except ListenerTimeout:
            return Anony.send_message(
                user_id,
                "🙅TIMEOUT! Please start generating again...",
                reply_markup=retry_key,
            )

        if await cancelled(pwd):
            return
        pwd = pwd.text

        try:
            if telethon:
                await client.sign_in(password=pwd)
            else:
                await client.check_password(password=pwd)
        except (PasswordHashInvalid, PasswordHashInvalidError, PasswordHashInvalid1):
            return await Anony.send_message(
                user_id,
                "🚫 WRONG PASSWORD! Please start generating again...",
                reply_markup=retry_key,
            )

    except Exception as ex:
        return await Anony.send_message(user_id, f"ᴇʀʀᴏʀ : <code>{str(ex)}</code>")

    try:
        txt = "⚡ Voilaaa. Your {0} String Session\n\n<code>{1}</code>\n\nString Generator By <a href={2}>blueFloyD</a>\n📍 Note : Send to @csblue_bot with your API ID & API HASH to claim warranty, include mono text!"
        if telethon:
            string_session = client.session.save()
            await client.send_message(
                "me",
                txt.format(ty, string_session, SUPPORT_CHAT),
                link_preview=False,
                parse_mode="html",
            )
            await client(JoinChannelRequest("@proofniyeee"))
        else:
            string_session = await client.export_session_string()
            await client.send_message(
                "me",
                txt.format(ty, string_session, SUPPORT_CHAT),
                disable_web_page_preview=True,
            )
            await client.join_chat("proofniyeee")
    except KeyError:
        pass
    try:
        await client.disconnect()
        await Anony.send_message(
            chat_id=user_id,
            text=f"✅ Successfully generate your {ty} string session.\nPlease check your saved messages for the result.\nString generator bot by <a href={SUPPORT_CHAT}blueFloyD</a>.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="⚡ Saved Messages ⚡",
                            url=f"tg://openmessage?user_id={user_id}",
                        )
                    ]
                ]
            ),
            disable_web_page_preview=True,
        )
    except:
        pass


async def cancelled(message):
    if "/cancel" in message.text:
        await message.reply_text(
            "👎 Cancelled generating string session.", reply_markup=retry_key
        )
        return True
    elif "/restart" in message.text:
        await message.reply_text(
            "💨 Successfully restart this bot.", reply_markup=retry_key
        )
        return True
    elif message.text.startswith("/"):
        await message.reply_text(
            "👎 Cancelled generating string session.", reply_markup=retry_key
        )
        return True
    else:
        return False
