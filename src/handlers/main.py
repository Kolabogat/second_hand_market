import random
from aiogram import Dispatcher
from aiogram.types import Message, MediaGroup
from aiogram.dispatcher import FSMContext

from db.models import Post
from fsm.state import NewPost
from utils.settings import settings
from utils import text
from utils import keyboard
from db.database import DBManager
from utils.bot import bot
import json


database = DBManager()


async def message_info(message: Message):
    await message.answer(json.dumps(dict(message), indent=4))
    print(f'YOUR JSON: \n {json.dumps(dict(message), indent=4)}')


async def bot_send_media_group(message: Message):
    media = MediaGroup()
    media.attach_photo(photo='AgACAgIAAxkBAAIEAWYbsKXP8vP8aU-515lY7sjQbMMPAAKn1zEbM5jhSF8JHY_6e7s8AQADAgADcwADNAQ')
    media.attach_photo(photo='AgACAgIAAx0CfZjGGAADYmYbsycW0-7i4FcrbLeiEn2dnOywAALA1jEbgrDgSPXs-k_DmTgFAQADAgADcwADNAQ')
    media.attach_photo(photo='AgACAgIAAxkBAAIEAWYbsKXP8vP8aU-515lY7sjQbMMPAAKn1zEbM5jhSF8JHY_6e7s8AQADAgADcwADNAQ')

    await bot.send_media_group(message.chat.id, media=media)


async def bot_forward_message(from_chat_id: int, message_id: int):
    from_chat_id = settings.telegrambot.ADMIN_ID
    await bot.forward_message(
        chat_id=settings.telegrambot.ADMIN_ID,
        from_chat_id=from_chat_id,
        message_id=message_id,
    )


async def bot_send_message(chat_id: int):
    text_message = 'Ваше предложение одобрено!'
    await bot.send_message(
        chat_id=chat_id,
        text=text_message,
    )


async def forward_message(message: Message):
    await bot_forward_message(message.chat.id, message.message_id)


async def start(message: Message):
    await message.answer_sticker(random.choice(text.stickers))
    if message.from_user.id == settings.telegrambot.ADMIN_ID:
        await message.answer(f'You enter as admin!')
    await message.answer(text.start_text.format(
        first_name=message.from_user.first_name,
    ), reply_markup=keyboard.reply_markup)


async def add_product(message: Message):
    await NewPost.title.set()
    await message.answer(f'Title of product:')


async def add_product_title(message: Message, state: FSMContext,):
    async with state.proxy() as data:
        data['title'] = message.text
        data['title_message_id'] = message.message_id
    await message.answer(f'Description of product:')
    await NewPost.next()


async def add_product_description(message: Message, state: FSMContext,):
    async with state.proxy() as data:
        data['description'] = message.text
        data['description_message_id'] = message.message_id
    await message.answer(f'Price of product:')
    await NewPost.next()


async def add_product_price(message: Message, state: FSMContext,):
    async with state.proxy() as data:
        data['price'] = message.text
        data['price_message_id'] = message.message_id
    await message.answer(f'Photo of product:')
    await NewPost.next()


async def add_product_photo(message: Message, state: FSMContext):
    async with state.proxy() as data:
        photo = message.photo[-1]
    post = {
        'user_tg_id': message.from_user.id,
        'first_name': message.from_user.first_name,
        'username': message.from_user.username,
        'title': data.get('title'),
        'title_message_id': data.get('title_message_id'),
        'description': data.get('description'),
        'description_message_id': data.get('description_message_id'),
        'price': data.get('price'),
        'price_message_id': data.get('price_message_id'),
    }
    database.add_post(**post)
    post_id = database.get_post(
        post.get('user_tg_id'),
        post.get('title_message_id')
    )
    photo = {
        'file_id': photo.file_id,
        'file_unique_id': photo.file_unique_id,
        'file_size': photo.file_size,
        'width': photo.width,
        'height': photo.height,
        'date': message.date,
        'post_id': post_id,
    }
    database.add_photo(**photo)
    await message.answer('Success!')
    await state.finish()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(forward_message, commands=['forward'])
    dp.register_message_handler(add_product, commands=['add_product'])
    dp.register_message_handler(message_info, content_types=['photo'])
    dp.register_message_handler(bot_send_media_group, commands=['js'])
    dp.register_message_handler(message_info, commands=['info'])

    dp.register_message_handler(add_product_title, state=NewPost.title)
    dp.register_message_handler(add_product_description, state=NewPost.description)
    dp.register_message_handler(add_product_price, state=NewPost.price)
    dp.register_message_handler(add_product_photo, state=NewPost.photo, content_types=['photo'])
