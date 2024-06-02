from db.database import DBManager
from settings.settings import settings

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


async def add_product_and_photo_to_db(message, state):
    post_data = await get_post_data_from_message(message, state)
    database.add_post(**post_data)
    post_id = database.get_post(
        post_data.get('user_tg_id'),
        post_data.get('title_message_id')
    )
    photo_data = await get_photo_data_from_message(message, state, post_id)
    database.add_photo(**photo_data)

