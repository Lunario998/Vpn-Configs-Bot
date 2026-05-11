from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()


@router.message(Command("get"))
async def get(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Черный список", callback_data="black")],
        [InlineKeyboardButton(text="Белый список", callback_data="white")],
        [InlineKeyboardButton(text="Обход глушилок", callback_data="bypass")],
    ])
    await message.answer(
        "Черный список — нужен когда работает всё кроме запрещённого: Ютуб, Дискорд, Телеграм, Тик ток.\n\n"
        "Белый список — нужен когда ничего не работает кроме разрешённого: Вконтакте, Яндекс, Банки, ГосУслуги.\n\n"
        "Обход глушилок — нужен когда провайдер блокирует VPN: спец конфиги для обхода глубоких блокировок.\n\n"
        "Выбери тип:", reply_markup=keyboard)
