from db.database import DBManager
from settings.settings import settings
from utils import text
from utils.bot import bot
from utils.keyboard import post_or_decline

database = DBManager()


def is_admin(func):
    async def wrapper(*args, **kwargs):
        user_id = dict(*args).get('from').get('id')
        if user_id == settings.telegrambot.ADMIN_ID:
            return await func(*args)
        return
    return wrapper


async def get_post_data_from_message(message, state):
    async with state.proxy() as data:
        post_data = {
            'user_tg_id': message.from_user.id,
            'first_name': message.from_user.first_name,
            'username': message.from_user.username,
            'title': data.get('title'),
            'title_message_id': data.get('title_message_id'),
            'description': data.get('description'),
            'description_message_id': data.get('description_message_id'),
            'price': data.get('price'),
            'price_message_id': data.get('price_message_id'),
            'contacts': data.get('contacts'),
            'contacts_message_id': data.get('contacts_message_id'),
        }
    return post_data


async def get_photo_data_from_message(message, state, post_id):
    async with state.proxy() as data:
        photo_object = data.get('photo')
        photo = {
            'date': message.date,
            'file_id': photo_object.file_id,
            'file_unique_id': photo_object.file_unique_id,
            'file_size': photo_object.file_size,
            'width': photo_object.width,
            'height': photo_object.height,
            'post_id': post_id,
        }
    return photo


async def send_product_to_admin(user_tg_id, title_message_id, photo):
    post = database.get_post(user_tg_id, title_message_id)
    await bot.send_photo(
        chat_id=settings.telegrambot.ADMIN_ID,
        photo=photo.file_id,
        caption=text.product_message.format(
            title=post.title,
            description=post.description,
            price=post.price,
            telegram_id=user_tg_id,
            contacts=post.contacts,
            user_tg_id=user_tg_id,
            title_message_id=title_message_id,
        ),
        reply_markup=post_or_decline,
    )


async def admin_forward_message(from_chat_id: int, message_id: int):
    await bot.forward_message(
        chat_id=settings.telegrambot.ADMIN_ID,
        from_chat_id=from_chat_id,
        message_id=message_id,
    )


async def group_copy_message(from_chat_id: int, message_id: int):
    await bot.copy_message(
        chat_id=settings.telegrambot.GROUP_ID,
        from_chat_id=from_chat_id,
        message_id=message_id,
    )
