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
from aiogram.types import InputFile

bot = Bot(token="7677925957:AAHnTPnKBn_84M9nsuwRIUi-3mUDsauaoQg")
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
    await message.answer("Выберите кнопку: ", reply_markup=kbd)

@dp.message_handler()
async def mes(message: types.Message):
    if message.text == "--->":
        await message.answer("Нажми 'голосовой помощник'!")
    elif message.text == "голосовой помощник":
        await message.answer("МОЛОДЕЦ")
    elif message.text == "<---":
        await message.answer("Нажми 'голосовой помощник'!")
    elif message.text == "сайт":
        await message.answer("https://rutube.ru/video/c6cc4d620b1d4338901770a44b3e82f4/")

@dp.message_handler(commands=["sendfile"])
async def cmd_send_file(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Документ"]
    keyboard.add(*buttons)
    await message.answer("Выберите тип файла:", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text in ["Документ"])
async def send_file_by_type(message: types.Message):
    chat_id = message.chat.id
    with open("bot1.py", "rb") as file:  # Убедитесь, что файл bot1.py существует в той же папке
        await bot.send_document(chat_id, file, caption="Вот ваш документ!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
'''
@dp.message_handler(content_types=types.ContentType.ANY)
async def gp(message: types.Message):
    await message.answer(message.chat.id,
                         golp ="newQ")# сюда экзешник голосового помощника


@dp.message_handler()
async def mes(message):
    bot.send_document(message.chat.id, ('filename.txt', file))

'''
executor.start_polling(dp, skip_updates=True)