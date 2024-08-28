from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import SUPPORT_CHAT


keyboard = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton(text="GENERATE SESSION!", callback_data="gensession")],
        [
            InlineKeyboardButton(text="SUPPORT", url=SUPPORT_CHAT),
            InlineKeyboardButton(
                text="SOURCE", url="https://t.me/proofniyeee"
            ),
        ],
    ]
)

gen_key = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="Pyrogram ver1", callback_data="pyrogram1"),
            InlineKeyboardButton(text="Pyrogram ver2", callback_data="pyrogram"),
        ],
        [InlineKeyboardButton(text="Telethon", callback_data="telethon")],
    ]
)

retry_key = InlineKeyboardMarkup(
    [[InlineKeyboardButton(text="Gen Session", callback_data="gensession")]]
)
