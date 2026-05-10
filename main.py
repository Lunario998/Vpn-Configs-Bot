import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import Token

logging.basicConfig(level=logging.INFO)

bot = Bot(token=Token)
dp = Dispatcher(storage=MemoryStorage())


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
