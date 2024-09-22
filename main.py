from aiogram import Bot, Dispatcher, types
from aiogram.methods import DeleteWebhook
from aiogram.client.bot import DefaultBotProperties
import asyncio
import logging
from config import TOKEN
from currency_converter import CurrencyConverter
from db import Database

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
c = CurrencyConverter()
dp = Dispatcher()
db = Database("database.db")


async def main():
    try:
        from handlers import dp
        await bot(DeleteWebhook(drop_pending_updates=True))
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())