import telebot
from aiogram import types

'''
from db_functions import put_abitur_into_db, put_student_into_db, get_all_faculties
from db_functions import get_recomendations, get_faculty, get_branches
from db_functions import get_brach_info, get_students
'''
from passwords import TOKEN

bot = telebot.TeleBot(TOKEN)


def interest_(message):
    pass


@bot.message_handler(commands=['start'])
async def start_welcome(message):
    bot.send_message(message.chat.id,
                     "Привет👋\nЧтобы помочь тебе с выбором, мы должны узнать о тебе немного.")
    await user_reg(message)


async def user_reg(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    itembtn1 = types.KeyboardButton("абитуриент")
    itembtn2 = types.KeyboardButton("представитель РЭУ")
    markup.add(itembtn1, itembtn2)

    bot.send_message(message.chat.id, 'Для начала, кто ты?')


@bot.message_handler(commands=["абитуриент"])
async def interest__(message):
    markup1 = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    itembtn1 = types.KeyboardButton("Информатика")
    itembtn2 = types.KeyboardButton("Математика")
    itembtn3 = types.KeyboardButton("Экономика и бизнес")
    itembtn4 = types.KeyboardButton("Управление")
    itembtn5 = types.KeyboardButton("Лингвистика")
    itembtn6 = types.KeyboardButton("Социальная сфера")
    itembtn7 = types.KeyboardButton("Другое")
    markup1.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7)

    bot.send_message(message.chat.id, 'Какое направление тебя интересует?')
    # bot.register_next_step_handler(msg, #следующий шаг)

    telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id,
                     'Поздравляю! Ты закнчил вводную часть. Теперь просто отмечай понравившиеся факультеты и '
                     'направления.\nСтуденты свяжутся с тобой!')


while True:
    try:
        bot.polling(none_stop=True)
    except OSError:
        bot.polling(none_stop=True)
