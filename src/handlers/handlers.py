import random
from aiogram import Dispatcher
from aiogram.types import Message, MediaGroup, CallbackQuery
from aiogram.dispatcher import FSMContext

from fsm.state import NewPost
from handlers.conf import (
    get_post_data_from_message,
    get_photo_data_from_message,
    is_admin, send_product_to_admin, group_copy_message, admin_forward_message
)
from settings.settings import settings
from utils import text
from utils import keyboard
from db.database import DBManager
from utils.bot import bot
import json


database = DBManager()


@is_admin
async def message_info(message: Message):
    await message.answer(json.dumps(dict(message), indent=4))
    print(f'YOUR JSON: \n {json.dumps(dict(message), indent=4)}')


@is_admin
async def send_sticker(message: Message):
    await message.answer_sticker('CAACAgIAAxkBAAIGKGZcbBuY3o2dYdXQzYyUPnLNVZtsAAI1AQACMNSdEbS4Nf1moLZ8NQQ')


@is_admin
async def bot_send_media_group(message: Message):
    media = MediaGroup()
    media.attach_photo(photo='AgACAgIAAxkBAAIEAWYbsKXP8vP8aU-515lY7sjQbMMPAAKn1zEbM5jhSF8JHY_6e7s8AQADAgADcwADNAQ')
    media.attach_photo(photo='AgACAgIAAx0CfZjGGAADYmYbsycW0-7i4FcrbLeiEn2dnOywAALA1jEbgrDgSPXs-k_DmTgFAQADAgADcwADNAQ')
    media.attach_photo(photo='AgACAgIAAxkBAAIEAWYbsKXP8vP8aU-515lY7sjQbMMPAAKn1zEbM5jhSF8JHY_6e7s8AQADAgADcwADNAQ')

    await bot.send_media_group(message.chat.id, media=media)


@is_admin
async def bot_send_message(chat_id: int):
    text_message = 'Ваше предложение одобрено!'
    await bot.send_message(
        chat_id=chat_id,
        text=text_message,
    )


@is_admin
async def forward_message(message: Message):
    await admin_forward_message(message.chat.id, message.message_id)


# @is_admin
async def get_chat_id(message: Message):
    await message.answer(message.chat.id)


async def start(message: Message):
    await message.answer_sticker(random.choice(text.stickers))
    if message.from_user.id == settings.telegrambot.ADMIN_ID:
        await message.answer(f'You enter as admin!')
    await message.answer(text.start_text.format(
        first_name=message.from_user.first_name,
    ), reply_markup=keyboard.reply_markup)


async def add_product_and_get_product_title(message: Message):
    await NewPost.title.set()
    await message.answer(f'Title of product:')


async def add_product_title_and_get_description(message: Message, state: FSMContext,):
    async with state.proxy() as data:
        data['title'] = message.text
        data['title_message_id'] = message.message_id
    await message.answer(f'Description of product:')
    await NewPost.next()


async def add_product_description_and_get_price(message: Message, state: FSMContext,):
    async with state.proxy() as data:
        data['description'] = message.text
        data['description_message_id'] = message.message_id
    await message.answer(f'Price of product:')
    await NewPost.next()


async def add_product_price_and_get_photo(message: Message, state: FSMContext,):
    async with state.proxy() as data:
        data['price'] = message.text
        data['price_message_id'] = message.message_id
    await message.answer(f'Photo of product:')
    await NewPost.next()


async def add_product_photo_and_commit_all(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1]
    post_data = await get_post_data_from_message(message, state)
    database.add_post(**post_data)
    post_id = database.get_post(
        post_data.get('user_tg_id'),
        post_data.get('title_message_id')
    )
    photo_data = await get_photo_data_from_message(message, state, post_id.id)
    database.add_photo(**photo_data)

    await send_product_to_admin(
        user_tg_id=message.from_user.id,
        title_message_id=data.get('title_message_id'),
        photo=data.get('photo'),
    )
    await message.answer('Success!')
    await state.finish()


async def callback_query_keyboard(callback_query: CallbackQuery):
    if callback_query.data == 'post':
        await group_copy_message(
            settings.telegrambot.ADMIN_ID,
            callback_query.message.message_id,
        )
    await bot.delete_message(
        settings.telegrambot.ADMIN_ID,
        callback_query.message.message_id
    )


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(add_product_and_get_product_title, commands=['add_product'])
    dp.register_callback_query_handler(callback_query_keyboard)

    dp.register_message_handler(get_chat_id, commands=['get_id'])
    dp.register_message_handler(forward_message, commands=['forward'])
    dp.register_message_handler(message_info, content_types=['sticker'])
    dp.register_message_handler(bot_send_media_group, commands=['js'])
    dp.register_message_handler(message_info, commands=['info'])
    dp.register_message_handler(send_sticker, commands=['sticker'])

    dp.register_message_handler(add_product_title_and_get_description, state=NewPost.title)
    dp.register_message_handler(add_product_description_and_get_price, state=NewPost.description)
    dp.register_message_handler(add_product_price_and_get_photo, state=NewPost.price)
    dp.register_message_handler(add_product_photo_and_commit_all, state=NewPost.photo)
    dp.register_message_handler(add_product_photo_and_commit_all, state=NewPost.photo, content_types=['photo'])
