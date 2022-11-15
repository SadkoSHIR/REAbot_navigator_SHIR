import sqlite3
import telebot
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage


TOKEN = ''
bot = telebot.TeleBot(TOKEN)


#хендлер для создания анкеты

class CreateProfile(StatesGroup):
	user_category = State()
	sphere = State()


@bot.message_handler(commands=['start'])
async def start(message : types.Message):
    if (not db.user_exists(message.from_user.id)):
        db.add_user(message.from_user.id)
        await message.answer('Привет👋\nЧтобы помочь тебе с выбором, мы должны узнать о тебе немного.', reply_markup=user_reg)
    else:
	    await bot.send_message(message.from_user.id, " эм вы уже зареганы?")


async def user_reg(state=CreateProfile.user_category, message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    itembtn1 = types.KeyboardButton("абитуриент")
    itembtn2 = types.KeyboardButton("представитель РЭУ")
    markup.add(itembtn1, itembtn2)

    msg = bot.send_message(message.chat.id, 'Для начала, кто ты?', reply_markup=markup)
    await CreateProfile.next()


@bot.message_handler(state=CreateProfile.sphere, commands=["представитель РЭУ"])
def interest(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    itembtn1 = types.KeyboardButton("Информатика")
    itembtn2 = types.KeyboardButton("Математика")
    itembtn3 = types.KeyboardButton("Экономика и бизнес")
    itembtn4 = types.KeyboardButton("Управление")
    itembtn5 = types.KeyboardButton("Лингвистика")
    itembtn6 = types.KeyboardButton("Социальная сфера")
    itembtn7 = types.KeyboardButton("Другое")
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7)

    msg = bot.send_message(message.chat.id, 'На каком направлении ты обучаешься?', reply_markup=markup)
    # bot.register_next_step_handler(msg, #следующий шаг)


@bot.message_handler(commands=["абитуриент"])
def interest(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn1 = types.KeyboardButton("Информатика")
    btn2 = types.KeyboardButton("Математика")
    btn3 = types.KeyboardButton("Общ")
    btn4 = types.KeyboardButton("Рус")
    btn5 = types.KeyboardButton("Англ")
    btn6 = types.KeyboardButton("Физика")
    btn7 = types.KeyboardButton("Другое")

    markup.row(btn1, btn2, btn3).add(bth7).row(btn4, btn5, btn6)

    msg = bot.send_message(message.chat.id, 'Какой предмет ЕГЭ ты планируешь сдавать?', reply_markup=markup)


