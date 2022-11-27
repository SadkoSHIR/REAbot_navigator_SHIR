import telebot
from aiogram import types

from db_functions import user_in_db, get_all_spheres, get_all_faculties
from db_functions import put_abitur_into_db, put_student_into_db
from db_functions import get_recomendations, get_faculty, get_branches
from db_functions import get_brach_info, get_students

from passwords import TOKEN

bot = telebot.TeleBot(TOKEN)
db =

@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id,
                     'Это бот-навигатор РЭУ. Он позволит Вам ознакомиться с факультетами и направлениями РЭУ, '
                     'а также лично пообщаться со студентами-представителями РЭУ. '
                     'А студенты могут помочь абитуриентам, рассказав о своих факультетах и направлениях '
                     'и ответив на вопросы абитуриента.\n\n'
                     'Нажмите /start чтобы зарегестрироваться или изменить уже внесенные данные.')


@bot.message_handler(commands=['start'])
def start_welcome(message):
    bot.send_message(message.chat.id,
                     "Привет👋\nЧтобы помочь тебе с выбором, мы должны узнать о тебе немного.")
    # await user_reg(message)
    user_registration(message)


def user_registration(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    itembtn1 = types.KeyboardButton("абитуриент")
    itembtn2 = types.KeyboardButton("студент")
    markup.add(itembtn1, itembtn2)

    bot.send_message(message.chat.id, 'Для начала, кто ты?',
                     reply_markup=[markup])


@bot.message_handler(content_types='text')
def text_message(message):
    print(message.text)
    if message.text == 'абитуриент':
        abiturient_registration(message)
    elif message.text == 'студент':
        student_registration(message)


def abiturient_registration(message):
    all_spheres = get_all_spheres()
    print(all_spheres)
    reply_keyboard = []
    for i in range(len(all_spheres[::2])):
        reply_keyboard.append([all_spheres[i], all_spheres[i + 1]])
    if len(all_spheres) % 2 == 1:
        reply_keyboard.append([all_spheres[-1]])

    markup = types.ReplyKeyboardMarkup(reply_keyboard,
                                       one_time_keyboard=True,
                                       resize_keyboard=True)

    bot.send_message(message.chat.id, 'Укажи, какая одна сфера тебя итнересует больше всего?',
                     reply_markup=[markup])
    # bot.register_next_step_handler(msg, #следующий шаг)

    telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id,
                     'Поздравляю! Ты закнчил вводную часть. Теперь просто отмечай понравившиеся факультеты и '
                     'направления.\nСтуденты свяжутся с тобой!')


def student_registration(message):
    bot.send_message(message.chat.id,
                     'Здесь скоро будет регистрация')


while True:
    try:
        bot.polling(none_stop=True)
    except OSError:
        bot.polling(none_stop=True)
