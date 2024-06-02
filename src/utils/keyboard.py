from utils.bot import bot
from aiogram.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Message
)

# Reply
reply_markup = ReplyKeyboardMarkup(resize_keyboard=True)
reply_markup.add('Add Product')


# Inline
post_or_decline = InlineKeyboardMarkup(row_width=2)
post_or_decline.add(
    InlineKeyboardButton(text='Post', callback_data='post'),
    InlineKeyboardButton(text='Reject', callback_data='reject'),
)
