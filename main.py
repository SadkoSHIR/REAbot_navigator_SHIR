from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from db_functions import put_abitur_into_db, put_student_into_db

import telebot
from aiogram import types
from aiogram.dispatcher import Dispatcher

TOKEN = ''
bot = telebot.TeleBot(TOKEN)
db = Dispatcher(bot)

hello_count = []


@db.message_handler(commands=['start'])
async def start(message: types.Message):
    if len(hello_count) == 0:
        bot.send_message(message.chat.id,
                         "Привет👋\nЧтобы помочь тебе с выбором, мы должны узнать о тебе немного.'")
        user_reg(message)
    else:
        interest_(message)
    hello_count.insert(1, 1)  # факт приветсвия


async def user_reg(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    itembtn1 = types.KeyboardButton("абитуриент")
    itembtn2 = types.KeyboardButton("представитель РЭУ")
    markup.add(itembtn1, itembtn2)

    bot.send_message(message.chat.id, 'Для начала, кто ты?')


@db.message_handler(commands=["представитель РЭУ"])
async def interest(message):
    markup1 = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    itembtn1 = types.KeyboardButton("Информатика")
    itembtn2 = types.KeyboardButton("Математика")
    itembtn3 = types.KeyboardButton("Экономика и бизнес")
    itembtn4 = types.KeyboardButton("Управление")
    itembtn5 = types.KeyboardButton("Лингвистика")
    itembtn6 = types.KeyboardButton("Социальная сфера")
    itembtn7 = types.KeyboardButton("Другое")
    markup1.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7)

    bot.send_message(message.chat.id, 'На каком направлении ты обучаешься?')
    # bot.register_next_step_handler(msg, #следующий шаг)


@db.message_handler(commands=["абитуриент"])
async def interest(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn1 = types.KeyboardButton("Информатика")
    btn2 = types.KeyboardButton("Математика")
    btn3 = types.KeyboardButton("Общ")
    btn4 = types.KeyboardButton("Рус")
    btn5 = types.KeyboardButton("Англ")
    btn6 = types.KeyboardButton("Физика")
    btn7 = types.KeyboardButton("Другое")
    btn8 = types.KeyboardButton("закончить")

    markup.row(btn1, btn2, btn3).row(btn4, btn5, btn6).add(btn8).add(btn7)

    if message.text == "Другое":
        interest_(message)

    elif message.text == "закончить":
        a = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id,
                         'Поздравляю! Ты закнчил вводную часть. Теперь просто отмечай понравившиеся факультеты и '
                         'направления.\nСтуденты свяжутся с тобой!',
                         reply_markup=a)


async def interest_(message):
    markup2 = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn1 = types.KeyboardButton("Химия")
    btn2 = types.KeyboardButton("Биология")
    btn3 = types.KeyboardButton("История")
    btn4 = types.KeyboardButton("География")
    btn5 = types.KeyboardButton("Литература")
    btn6 = types.KeyboardButton("закончить")
    btn7 = types.KeyboardButton("Другoе")

    markup2.row(btn1, btn2, btn3).row(btn4, btn5).add(btn7).add(btn6)

    if message.text == "Другoе":
        interest(message)
    elif message.text == "закончить":
        a = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id,
                         'Поздравляю! Ты закнчил вводную часть. Теперь просто отмечай понравившиеся факультеты и '
                         'направления.\nСтуденты свяжутся с тобой!',
                         reply_markup=a)


while True:
    try:
        bot.polling(none_stop=True)
    except OSError:
        bot.polling(none_stop=True)
