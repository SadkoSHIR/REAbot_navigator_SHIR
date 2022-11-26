import telebot
from aiogram import types

'''
from db_functions import put_abitur_into_db, put_student_into_db, get_all_faculties
from db_functions import get_recomendations, get_faculty, get_branches
from db_functions import get_brach_info, get_students
'''
from passwords import TOKEN

bot = telebot.TeleBot(TOKEN)


def get_spheres():
    return ['Информатика', 'Экономика', 'Математика', 'Управление', 'Другое']


def interest_():
    pass


@bot.message_handler(commands=['start'])
def start_welcome(message):
    msg = bot.send_message(message.chat.id,
                           "Привет👋\nЧтобы помочь тебе с выбором, мы должны узнать о тебе немного.")
    bot.register_next_step_handler(msg, user_reg)


async def user_reg(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    itembtn1 = types.KeyboardButton("абитуриент")
    itembtn2 = types.KeyboardButton("представитель РЭУ")
    markup.add(itembtn1, itembtn2)
    bot.send_message(message.chat.id, 'Для начала, кто ты?')


@bot.message_handler(contest_types=["абитуриент"])
async def interest__(message):
    markup1 = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    ss = get_spheres()
    spheres = []
    for i in ss:
        spheres.append(types.KeyboardButton(i))

    markup1.add(spheres)

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
