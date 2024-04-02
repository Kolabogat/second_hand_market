import random
from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from db.models import Post
from fsm.state import NewPost
from utils.settings import settings
from utils import text
from utils import keyboard
from db.database import DBManager


database = DBManager()


async def start(message: Message):
    await message.answer_sticker(random.choice(text.stickers))
    if message.from_user.id == settings.super_bot.ADMIN_ID:
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
    await message.answer(f'Success!')  # Message of ticket
    await NewPost.next()








def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(add_product, commands=['add_product'])
    dp.register_message_handler(add_product_title, state=NewPost.title)
    dp.register_message_handler(add_product_description, state=NewPost.description)
    dp.register_message_handler(add_product_price, state=NewPost.price)

