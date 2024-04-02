from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from utils.settings import settings

storage = MemoryStorage()

bot = Bot(settings.super_bot.bot_token)
dp = Dispatcher(bot, storage=storage)



