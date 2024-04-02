from aiogram import Dispatcher, executor
from utils.bot import dp
from db.database import create_all
import logging

from handlers.main import register_handlers

logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - [%(levelname)s] - %(name)s - '
               '(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s',
    )


async def on_startup(_: Dispatcher):
    create_all()
    print('Bot started')


if __name__ == '__main__':
    register_handlers(dp)
    executor.start_polling(
        dp,
        skip_updates=True,
        on_startup=on_startup,
        allowed_updates=['message', 'callback_query'],
    )
