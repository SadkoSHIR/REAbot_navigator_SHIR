import sqlite3
import telebot
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton


TOKEN = ''
bot = telebot.TeleBot(TOKEN)


def gen_main_markup():
    markup = ReplyKeyboardMarkup()
    markup.add()

@bot.message_handler(commands=['start'])
def user_reg(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    itembtn1 = types.KeyboardButton("абитуриент")
    itembtn2 = types.KeyboardButton("представитель РЭУ")
    markup.add(itembtn1, itembtn2)

    msg = bot.send_message(message.chat.id, 'Кто ты?', reply_markup=markup)


@bot.message_handler(commands=["представитель РЭУ"])
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
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    itembtn1 = types.KeyboardButton("Информатика")
    itembtn2 = types.KeyboardButton("Математика")
    itembtn3 = types.KeyboardButton("Экономика и бизнес")
    itembtn4 = types.KeyboardButton("Управление")
    itembtn5 = types.KeyboardButton("Лингвистика")
    itembtn6 = types.KeyboardButton("Социальная сфера")
    itembtn7 = types.KeyboardButton("Другое")
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7)

    msg = bot.send_message(message.chat.id, 'Какое направление тебя сейчас интересует?', reply_markup=markup)
