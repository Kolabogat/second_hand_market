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
    await message.answer(f'Description of product:')
    await NewPost.next()


async def add_product_description(message: Message, state: FSMContext,):
    async with state.proxy() as data:
        data['description'] = message.text
    await message.answer(f'Price of product:')
    await NewPost.next()


async def add_product_price(message: Message, state: FSMContext,):
    async with state.proxy() as data:
        data['price'] = message.text
    database.add_post(
        user_tg_id=message.from_user.id,
        title=data.get('title'),
        description=data.get('description'),
        price=data.get('price'),
    )
    await message.answer(f'Photo of product:')  # Message of ticket
    await NewPost.next()


async def add_product_photo(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id
    await message.bot.download_file(file_path=message.photo[-1].file_id, destination='file_name')
    # await database.add_photo(message.message.photo[-1])
    await message.answer('Success', reply_markup=settings.telegrambot.ADMIN_ID)
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
