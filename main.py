import telebot
from aiogram import types

from db_functions import user_in_db, get_all_spheres, get_all_faculties
from db_functions import put_abitur_into_db, put_student_into_db
from db_functions import get_recomendations, get_faculty, get_branches
from db_functions import get_brach_info, get_students

from passwords import TOKEN

bot = telebot.TeleBot(TOKEN)


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

    bot.send_message(message.chat.id, 'Укажи, какая одна сфера тебя интересует больше всего?',
                     reply_markup=[markup])
    # bot.register_next_step_handler(msg, #следующий шаг)

    telebot.types.ReplyKeyboardRemove()

    if (not user_in_db(message.from_user.id)):
        put_abitur_into_db(message.from_user.username, message.text)

    msg = bot.send_message(message.chat.id,
                     'Поздравляю! Ты закончил вводную часть. Теперь просто отмечай понравившиеся факультеты и '
                     'направления.\nСтуденты свяжутся с тобой!')

    bot.register_next_step_handler(msg, abiturient_recomendations)
    if (not user_in_db(message.from_user.id)):
        put_abitur_into_db(message.from_user.username, message.text)


# def abiturient_recomendations(message):
#     recomendations = get_recomendations()
#     print(recomendations)
#     reply_keyboard = []
#     for i in range(len(recomendations[::2])):
#         reply_keyboard.append([recomendations[i], recomendations[i + 1]])
#     if len(recomendations) % 2 == 1:
#         reply_keyboard.append([recomendations[-1]])
#
#     markup = types.ReplyKeyboardMarkup(reply_keyboard,
#                                        one_time_keyboard=True,
#                                        resize_keyboard=True)
#
#     bot.send_message(message.chat.id, 'Укажи, какой факультет тебе интересен?\nЯ о нём расскажу.',
#                      reply_markup=[markup])


def student_registration(message: types.Message):
    bot.send_message(message.chat.id, 'Напиши свой юзернейм в формате @vasyapupkin')
    if message.text:
        global student_username = message.text
        student_registration_2(message)

def student_registration_2(message):
    all_faculties = get_all_faculties()
    print(all_faculties)
    reply_keyboard = []
    for i in range(len(all_faculties[::2])):
        reply_keyboard.append([all_faculties[i], all_faculties[i + 5]])
    if len(all_faculties) % 2 != 0:
        reply_keyboard.append([all_faculties[i-2]])

    markup = types.ReplyKeyboardMarkup(reply_keyboard,
                                           one_time_keyboard=True,
                                           resize_keyboard=True)

    bot.send_message(message.chat.id, 'Укажи, в каком факультете ты обучаешься?',
                         reply_markup=[markup])
    global student_fac = message.text

        all_branches = get_branches()
        print(all_branches)
        reply_keyboard = []
        for i in range(len(all_branches[::2])):
            reply_keyboard.append([all_branches[i], all_branches[i + 5]])
        if len(all_branches) % 2 != 0:
            reply_keyboard.append([all_branches[i - 2]])

        markup = types.ReplyKeyboardMarkup(reply_keyboard,
                                           one_time_keyboard=True,
                                           resize_keyboard=True)

        bot.send_message(message.chat.id, 'Укажи, на каком направлеии ты обучаешься?',
                         reply_markup=[markup])

        telebot.types.ReplyKeyboardRemove()
        student_branch = message.text

        bot.send_message(message.chat.id,
                         'Поздравляю! Ты закончил вводную часть. Теперь жди абитуриентов, нуждающихся в твоей помощи.')


        if (not user_in_db(message.from_user.id)):
            put_student_into_db(student_username, student_fac, student_branch)


while True:
    try:
        bot.polling(none_stop=True)
    except OSError:
        bot.polling(none_stop=True)
