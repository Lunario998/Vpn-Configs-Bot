from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from config import Github_Black_Full, Github_Black_Mobile, Github_White_Full, Github_White_Mobile, Github_Bypass
from utils.fetcher import fetch_configs
from utils.validator import find_working_config

router = Router()

Url = {
    "black_full": Github_Black_Full,
    "black_mobile": Github_Black_Mobile,
    "white_full": Github_White_Full,
    "white_mobile": Github_White_Mobile,
    "bypass": Github_Bypass,
}


@router.callback_query(lambda c: c.data == "black")
async def black_list(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Полное покрытие", callback_data="black_full")],
        [InlineKeyboardButton(text="Мобильный", callback_data="black_mobile")],
    ])
    await callback.message.edit_text("Черный список — выбери:", reply_markup=keyboard)
    await callback.answer()


@router.callback_query(lambda c: c.data == "white")
async def white_list(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Полное покрытие", callback_data="white_full")],
        [InlineKeyboardButton(text="Мобильный", callback_data="white_mobile")],
    ])
    await callback.message.edit_text("Белый список — выбери:", reply_markup=keyboard)
    await callback.answer()


@router.callback_query(lambda c: c.data == "bypass")
async def bypass_list(callback: CallbackQuery):
    url = Github_Bypass

    if not url:
        await callback.message.edit_text("Ссылка не настроена.")
        await callback.answer()
        return

    await callback.message.edit_text("Ищу рабочий конфиг...")

    configs = await fetch_configs(url)
    if not configs:
        await callback.message.edit_text("Не удалось загрузить конфиги.")
        await callback.answer()
        return

    working = await find_working_config(configs)
    if not working:
        await callback.message.edit_text("Рабочих конфигов не найдено.")
        await callback.answer()
        return

    text = f"Рабочий конфиг:\n\n<code>{working[0]}</code>"
    if len(working) >= 2:
        text += f"\n\nЗапасной:\n\n<code>{working[1]}</code>"

    await callback.message.edit_text(text, parse_mode="HTML")
    await callback.answer()


@router.callback_query(lambda c: c.data in Url)
async def give_config(callback: CallbackQuery):
    url = Url[callback.data]

    if not url:
        await callback.message.edit_text("Ссылка не настроена.")
        await callback.answer()
        return

    await callback.message.edit_text("Ищу рабочий конфиг...")

    configs = await fetch_configs(url)
    if not configs:
        await callback.message.edit_text("Не удалось загрузить конфиги.")
        await callback.answer()
        return

    working = await find_working_config(configs)
    if not working:
        await callback.message.edit_text("Рабочих конфигов не найдено.")
        await callback.answer()
        return

    text = f"Рабочий конфиг:\n\n<code>{working[0]}</code>"
    if len(working) >= 2:
        text += f"\n\nЗапасной:\n\n<code>{working[1]}</code>"

    await callback.message.edit_text(text, parse_mode="HTML")
    await callback.answer()
