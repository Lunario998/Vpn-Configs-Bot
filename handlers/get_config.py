from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from utils.fetcher import fetch_configs
from utils.validator import find_working_config

router = Router()


@router.message(Command("get"))
async def get(message: Message):
    wait_msg = await message.answer("Ищу рабочий конфиг...")

    configs = await fetch_configs()
    if not configs:
        await wait_msg.edit_text("Не удалось загрузить конфиги.")
        return

    working = await find_working_config(configs)
    if not working:
        await wait_msg.edit_text("Рабочих конфигов не найдено.")
        return

    await wait_msg.edit_text(f"Вот рабочий конфиг:\n\n<code>{working}</code>", parse_mode="HTML")
