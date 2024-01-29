import asyncio
import logging
import sys

import openai

from aiogram import Bot, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message, ReplyKeyboardRemove

from aiogram import Bot, Dispatcher, Router, types
from aiogram import types
from aiogram.filters import CommandStart, Command
from aiogram.utils.markdown import hbold

import states
from conf import TOKEN, dp
from db import add_user, add_user_name, add_user_age, add_user_city, log
from states import Reg


@dp.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    chat_id = message.chat.id
    add_user(message)
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!"
                         f" Я Тестовый бот, что бы узнать на что я способен отправь /help")


HELP = """
/start - приветствие
/help - основной функционал бота
/registration - пошаговая запись твоего ФИО
"""


@dp.message(Command('help'))
async def command_help(message: types.Message) -> None:
    await message.answer(HELP)


# =====
kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Отменить')
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


@dp.message(Command("cancel"))
@dp.message(F.text.casefold() == "Отменить")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)
    await state.clear()
    await message.answer(
        "Cancelled.",
        reply_markup=ReplyKeyboardRemove(),
    )


@dp.message(Command('registration'))
async def bot_register(message: Message, state: FSMContext) -> None:
    await state.set_state(Reg.name)
    await message.answer(f'Для регистрации введи свое ФИО:',
                         reply_markup=kb)


@dp.message(Reg.name)
async def get_name(message: types.Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    add_user_name(message)
    await state.set_state(Reg.age)
    await message.answer(f'*{message.text}*, отлично! Теперь напиши свой возраст.',
                         reply_markup=kb)


@dp.message(Reg.age)
async def get_age(message: types.Message, state: FSMContext) -> None:
    await state.update_data(age=message.text)
    add_user_age(message)
    await message.answer('Последний шаг: где ты живешь?',
                         reply_markup=kb)
    await state.set_state(Reg.city)


@dp.message(Reg.city)
async def get_city(message: types.Message, state: FSMContext) -> None:
    await state.update_data(city=message.text)
    add_user_city(message)
    data = await state.get_data()
    name = data.get('name')
    age = data.get('age')
    city = data.get('city')
    await state.clear()
    await message.answer(f'Регистрация успещно завершина.\n'
                         f'ФИО: {name}\n'
                         f'Возраст: {age}\n'
                         f'Город: {city}\n')


# =====


@dp.message()
async def logs(message: types.Message):
    log(message)


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
