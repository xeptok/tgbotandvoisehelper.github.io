from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils.markdown import *
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import pandas as pd

bot = Bot(token="7679500988:AAFh3JkVwGDD4OJBsUcMZb4x3M1_nxeP59I")
dp = Dispatcher(bot)

btn1 = KeyboardButton("--->")
btn2 = KeyboardButton("голосовой помощник")
btn3 = KeyboardButton("<---")
btn4 = KeyboardButton("сайт")
kbd = ReplyKeyboardMarkup(resize_keyboard=True)
kbd.row(btn1, btn2, btn3)
kbd.add(InlineKeyboardButton(text="сайт", url="https://rutube.ru/video/c6cc4d620b1d4338901770a44b3e82f4/"))



urlkbd = InlineKeyboardMarkup(row_width=1)
urlbtn1 = InlineKeyboardButton(text = "--->", callback_data="Нажми 'голосовой помощник!'")
urlbtn2 = InlineKeyboardButton(text = "голосовой помощник", callback_data="игра1")
urlbtn3 = InlineKeyboardButton(text = "<---", callback_data="Нажми 'голосовой помощник!'")
urlkbd.add(urlbtn1).add(urlbtn2).add(urlbtn3)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Выберите кнопку: \n"
                         "введите: 'команды' для большей информации ", reply_markup=kbd)

@dp.message_handler()
async def intro(message: types.Message):
    if message.text == "--->":
        await message.answer("Нажми 'голосовой помощник!'")
    elif message.text == "голосовой помощник":
            await message.answer("МОЛОДЕЦ")
    elif message.text == "<---":
        await message.answer("Нажми 'голосовой помощник!'")
    elif message.text == "сайт":
        await message.answer("https://rutube.ru/video/c6cc4d620b1d4338901770a44b3e82f4/")

@dp.message_handler(content_types=types.ContentType.ANY)
async def gp(message: types.Message):
    await message.answer(message.chat.id,
                         golp = )# сюда экзешник голосового помощника

executor.start_polling(dp, skip_updates=True)