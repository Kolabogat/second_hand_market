from aiogram.dispatcher.filters.state import State, StatesGroup


class NewPost(StatesGroup):
    title = State()
    description = State()
    price = State()
    photo = State()

