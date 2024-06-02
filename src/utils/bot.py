from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from settings.settings import settings

storage = MemoryStorage()

bot = Bot(settings.telegrambot.BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)



