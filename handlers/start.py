from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "Даров я бот для выдачи рабочих VPN конфигов\n"
        "Нажми /get чтобы получить рабочий конфиг"
    )
