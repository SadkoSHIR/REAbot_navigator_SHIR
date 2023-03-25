import telebot
from aiogram import types

from db_functions import user_in_db, get_all_spheres, get_all_faculties
from db_functions import put_abitur_into_db, put_student_into_db
from db_functions import get_recomendations, get_faculty, get_branches
from db_functions import get_brach_info, get_students, get_rec_branches

from recomendations import RecommendModel, Anketa

from passwords import TOKEN

bot = telebot.TeleBot(TOKEN)
# student_fac = ''
# recommends = []
# rec_brs = []
# cur, fac, br = 'fac', 0, 0

RecommendModel.create_model()
Anketa.create_anketa()

users = {}


class User:
    def __init__(self, type):
        self.type = type
        self.student_fac = ''
        self.recommends = []
        self.rec_brs = []
        self.cur = 'fac'
        self.fac = 0
        self.br = 0
        self.state = 'none'
        self.anketa_ind = -1
        self.anketa = []


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
    if user_in_db(message.from_user.id):
        bot.send_message(message.chat.id,
                         "Ты уже зарегистрирован в нашей системе. Пока это можно сделать только один раз.")
        return

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    itembtn1 = types.KeyboardButton("абитуриент")
    itembtn2 = types.KeyboardButton("студент")
    markup.add(itembtn1, itembtn2)

    bot.send_message(message.chat.id, 'Для начала, кто ты?',
                     reply_markup=[markup])


@bot.message_handler(content_types='text')
def text_message(message):
    try:
        # # print('message.text', message.text)
        # print('users', users)
        # global student_fac
        # global recommends, cur, fac, br, rec_brs
        if message.chat.id in users and users[message.chat.id].state == 'anketa':
            if message.text.isdigit():

                users[message.chat.id].anketa.append(int(message.text))

                if users[message.chat.id].anketa_ind < 10:
                    # get next question
                    users[message.chat.id].anketa_ind += 1
                    bot.send_message(message.chat.id,
                                     Anketa.get_question(users[message.chat.id].anketa_ind))
                else:
                    # get recommendation
                    users[message.chat.id].state = 'none'
                    recommend = RecommendModel.get_recommendation(users[message.chat.id].anketa)
                    abiturient_registration(message, recommend)
            else:
                bot.send_message(message.chat.id,
                                 'Надо ввести число:')

        elif message.text == 'абитуриент':
            user = User(message.text)
            users[message.chat.id] = user

            abiturient_quest(message)

        elif message.text == 'студент':
            user = User(message.text)
            users[message.chat.id] = user

            student_registration(message)

        elif message.text in get_all_spheres():
            # print('Before user_in_db ', message.from_user.id)
            if not user_in_db(message.from_user.id):
                put_abitur_into_db(message.from_user.id, message.text)

            bot.send_message(message.chat.id,
                             'Поздравляю! Ты закончил вводную часть. Теперь просто отмечай понравившиеся факультеты.')

            # abiturient_recomendations(message)

            telebot.types.ReplyKeyboardRemove()

            users[message.chat.id].recommends = get_recomendations(message.from_user.id)
            # print('recommends', users[message.chat.id].recommends)
            send_recommendations(message)
            users[message.chat.id].cur = 'fac'
            users[message.chat.id].fac = 0
            users[message.chat.id].br = 0

        elif message.text in get_all_faculties():
            users[message.chat.id].student_fac = message.text
            student_registration_finish(message)

        elif message.text in get_branches(users[message.chat.id].student_fac):
            student_branch = message.text

            bot.send_message(message.chat.id,
                             'Поздравляю! Ты закончил вводную часть. '
                             'Теперь жди абитуриентов, нуждающихся в твоей помощи.')

            if not user_in_db(message.from_user.id):
                put_student_into_db(message.from_user.id, users[message.chat.id].student_fac, student_branch)

        elif message.text == 'Интересует':
            if users[message.chat.id].cur == 'fac':
                users[message.chat.id].cur = 'br'
                users[message.chat.id].rec_brs = get_rec_branches(users[message.chat.id].recommends[users[message.chat.id].fac])
                # print('rec_brs', users[message.chat.id].rec_brs)
                bot.send_message(message.chat.id,
                                 'Отлично, теперь отмечай понравившиеся направления на этой высшей школе.'
                                 '\nСтуденты свяжутся с тобой!')

                send_recommendations(message)
            elif users[message.chat.id].cur == 'br':
                bot.send_message(message.chat.id,
                                 '<i>Ваша заявка отправлена соответствующим студентам</i>', parse_mode='HTML')
                bot.send_message(message.chat.id,
                                 'Теперь продолжаем!')
                send_student_request(message)
                if users[message.chat.id].br + 1 == len(users[message.chat.id].rec_brs):
                    if users[message.chat.id].fac + 1 == len(users[message.chat.id].recommends):
                        bot.send_message(message.from_user.id, 'На этом пока все! Спасибо за участие')
                        del users[message.chat.id]
                        return
                    users[message.chat.id].cur = 'fac'
                    users[message.chat.id].fac += 1
                    users[message.chat.id].br = 0
                    bot.send_message(message.from_user.id,
                                     'На этом все, направления на этом факультете закончились. '
                                     'Я продолжу тебе присылать другие факультеты.')

                else:
                    users[message.chat.id].br += 1
                send_recommendations(message)

        elif message.text == 'Не интересует':
            if users[message.chat.id].cur == 'fac':
                if users[message.chat.id].fac + 1 == len(users[message.chat.id].recommends):
                    bot.send_message(message.from_user.id, 'На этом пока все! Спасибо за участие')
                    del users[message.chat.id]
                    return
                users[message.chat.id].fac += 1
                send_recommendations(message)
            elif users[message.chat.id].cur == 'br':
                if users[message.chat.id].br + 1 == len(users[message.chat.id].rec_brs):
                    users[message.chat.id].cur = 'fac'
                    users[message.chat.id].fac += 1
                    users[message.chat.id].br = 0
                    bot.send_message(message.from_user.id,
                                     'На этом все, направления на этом факультете закончились. '
                                     'Я продолжу тебе присылать другие факультеты.')

                else:
                    users[message.chat.id].br += 1
                send_recommendations(message)

    except Exception as e:
        print(repr(e))
        bot.send_message(message.from_user.id, 'На этом пока все! Спасибо за участие')


def abiturient_quest(message):
    users[message.chat.id].state = 'anketa'
    users[message.chat.id].anketa_ind = 1

    bot.send_message(message.from_user.id,
                     'Пройди небольшой опрос, чтобы мы смогли порекомендовать тебе направление обучения.\n'
                     '<u>Ответ на вопрос это число от 1 до 10</u> в соответствии с верностью утверждения.\n\n',
                     parse_mode='HTML')
    bot.send_message(message.from_user.id,
                     Anketa.get_question(1), reply_markup=False)


def abiturient_registration(message, recommend):
    all_spheres = get_all_spheres()
    # print('all_spheres', all_spheres)
    reply_keyboard = []
    for i in range(len(all_spheres[::2])):
        reply_keyboard.append([all_spheres[i], all_spheres[i + 3]])
    if len(all_spheres) % 2 == 1:
        reply_keyboard.append([all_spheres[-1]])

    markup = types.ReplyKeyboardMarkup(reply_keyboard,
                                       one_time_keyboard=True,
                                       resize_keyboard=True)

    bot.send_message(message.chat.id,
                     'Наша рекоммендация: ' + '<b>'+recommend+'</b>', parse_mode='HTML')
    bot.send_message(message.chat.id,
                     '\n\nТеперь укажи, какая одна сфера тебя интересует больше всего?',
                     reply_markup=[markup])
    # bot.register_next_step_handler(msg, #следующий шаг)


def student_registration(message):
    all_faculties = get_all_faculties()
    # print('all_faculties', all_faculties)
    reply_keyboard = []
    for i in range(len(all_faculties[::2])):
        reply_keyboard.append([all_faculties[i], all_faculties[i + 5]])
    if len(all_faculties) % 2 != 0:
        reply_keyboard.append([all_faculties[i-2]])

    markup = types.ReplyKeyboardMarkup(reply_keyboard,
                                           one_time_keyboard=True,
                                           resize_keyboard=True)

    bot.send_message(message.chat.id, 'Укажи, на каком факультете ты обучаешься?',
                         reply_markup=[markup])


def student_registration_finish(message):
    # global student_fac
    all_branches = get_branches(users[message.chat.id].student_fac)
    # print('all_branches', all_branches)
    reply_keyboard = []
    for i in range(len(all_branches[:len(all_branches)-1:2])):
        reply_keyboard.append([all_branches[i], all_branches[i + len(all_branches) // 2]])
    if len(all_branches) % 2 == 1:
        reply_keyboard.append([all_branches[-1]])

    markup = types.ReplyKeyboardMarkup(reply_keyboard,
                                       one_time_keyboard=True,
                                       resize_keyboard=True)

    bot.send_message(message.chat.id, 'Укажи, на каком направлении ты обучаешься?',
                     reply_markup=[markup])

    telebot.types.ReplyKeyboardRemove()


def send_recommendations(message):
    # global recommends
    # global cur, fac, br
    if users[message.chat.id].cur == 'fac':  # сейчас присылаем факультет
        markup = types.ReplyKeyboardMarkup([['Интересует', 'Не интересует']],
                                           one_time_keyboard=True,
                                           resize_keyboard=True)
        s = get_faculty(users[message.chat.id].recommends[users[message.chat.id].fac])[1:]
        rrecs = f'{s[0]}\n<b>{s[2]}</b>\n\n{s[1]}'
        # bot.send_message(message.chat.id, rrecs,
        #                  reply_markup=[markup])
        bot.send_photo(message.chat.id,
                       photo=open('images/'+str(users[message.chat.id].recommends[users[message.chat.id].fac])+'.jpg', 'rb'),
                       caption=rrecs, parse_mode='HTML',
                       reply_markup=[markup])
    elif users[message.chat.id].cur == 'br':
        markup = types.ReplyKeyboardMarkup([['Интересует', 'Не интересует']],
                                           one_time_keyboard=True,
                                           resize_keyboard=True)
        s = get_brach_info(users[message.chat.id].rec_brs[users[message.chat.id].br])[1:2] + get_brach_info(users[message.chat.id].rec_brs[users[message.chat.id].br])[4:]
        progs = '\n'.join(list(' - '+x for x in s[1].split(' - ')))
        egs = '\n'.join(list(' - '+x for x in s[2].split(' - ')))
        rrecs = f'<u>Направление:</u> <b>{s[0]}</b>\n\n<u>Программы:</u>\n{progs}\n\n<u>ЕГЭ:</u>\n{egs}'
        bot.send_message(message.chat.id, rrecs, parse_mode='HTML',
                         reply_markup=[markup])


def send_student_request(message):
    students = get_students(users[message.chat.id].rec_brs[users[message.chat.id].br])
    # print('students', students)
    if message.from_user.username and students:
        for id in students:
            # print(id)
            bot.send_message(id, f'Абитуриент https://t.me/{message.from_user.username} хочет получить консультацию. '
                                 f'Напиши ему и ответь на интересующие вопросы!')


while True:
    try:
        bot.polling(none_stop=True)
    except OSError:
        bot.polling(none_stop=True)
