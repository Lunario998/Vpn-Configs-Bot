import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import Token

logging.basicConfig(level=logging.INFO)

bot = Bot(token=Token)
dp = Dispatcher(storage=MemoryStorage())


async def main():
    from handlers import start, get_config, callbacks
    dp.include_router(start.router)
    dp.include_router(get_config.router)
    dp.include_router(callbacks.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
