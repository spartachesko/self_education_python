import datetime
import math

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from token_petrovich import token

"""
Модуль telegram.ext содержит много классов, 
но самые важные — telegram.ext.Updater и 
telegram.ext.Dispatcher. Updater отвечает за выборку 
новых обновлений от Telegram. Также он передает их в Dispatcher, 
после чего они обрабатываются с помощью Handler."""

STATE = None
BIRTH_YEAR = 1
BIRTH_MONTH = 2
BIRTH_DAY = 3


# function to handle the /start command
def start(update, context):
    first_name = update.message.from_user.first_name
    update.message.reply_text(f"Привет {first_name}, нужны твои данные!")
    start_getting_birthday_info(update, context)


def start_getting_birthday_info(update, context):
    global STATE
    STATE = BIRTH_YEAR
    update.message.reply_text(
        f"Мне бы твой год рождения узнать...")


def received_birth_year(update, context):
    global STATE

    try:
        today = datetime.date.today()
        text_str = update.message.text[1:]
        year = int(text_str)

        if year > today.year:
            raise ValueError("Ты ошибся!")

        context.user_data['birth_year'] = year
        update.message.reply_text(
            f"Ладно. Теперь нужен месяц твоего рождения(цифрами)...")

        STATE = BIRTH_MONTH

    except:
        update.message.reply_text(
            "Печатай без ошибок!")


def received_birth_month(update, context):
    global STATE

    try:
        today = datetime.date.today()
        text_str = update.message.text[1:]
        month = int(text_str)

        if month > 12 or month < 1:
            raise ValueError("Опять ты ошибся. Повтори ввод")

        context.user_data['birth_month'] = month
        update.message.reply_text(f"Отлично!И теперь день...")
        STATE = BIRTH_DAY
    except:
        update.message.reply_text(
            "Повтори...Опять ошибка в вводе")


def received_birth_day(update, context):
    global STATE

    try:
        today = datetime.date.today()
        text_str = update.message.text[1:]
        dd = int(text_str)
        yyyy = context.user_data['birth_year']
        mm = context.user_data['birth_month']
        birthday = datetime.date(year=yyyy, month=mm, day=dd)

        if today - birthday < datetime.timedelta(days=0):
            raise ValueError("Некорректный ввод!")

        context.user_data['birthday'] = birthday
        STATE = None
        update.message.reply_text(f'Как я понял, ты родился {birthday}')

    except:
        update.message.reply_text(
            "Некорректный ввод!")


# function to handle the /help command
def help(update, context):
    update.message.reply_text('Ты просишь меня помочь тебе?')


# function to handle errors occured in the dispatcher
def error(update, context):
    update.message.reply_text('Сбои во мне!')


# function to handle normal text
def text(update, context):
    global STATE
    if STATE == BIRTH_YEAR:
        return received_birth_year(update, context)

    if STATE == BIRTH_MONTH:
        return received_birth_month(update, context)

    if STATE == BIRTH_DAY:
        return received_birth_day(update, context)


# This function is called when the /biorhythm command is issued
def biorhythm(update, context):
    print("ok")
    user_biorhythm = calculate_biorhythm(
        context.user_data['birthday'])

    update.message.reply_text(f"Твой физический биоритм: {user_biorhythm['phisical']}")
    update.message.reply_text(f"Твой эмоциональный биоритм: {user_biorhythm['emotional']}")
    update.message.reply_text(f"Твой интеллектуальный биоритм: {user_biorhythm['intellectual']}")


def calculate_biorhythm(birthdate):
    today = datetime.date.today()
    delta = today - birthdate
    days = delta.days

    phisical = math.sin(2 * math.pi * (days / 23))
    emotional = math.sin(2 * math.pi * (days / 28))
    intellectual = math.sin(2 * math.pi * (days / 33))

    biorhythm = {}
    biorhythm['phisical'] = int(phisical * 10000) / 100
    biorhythm['emotional'] = int(emotional * 10000) / 100
    biorhythm['intellectual'] = int(intellectual * 10000) / 100

    biorhythm['phisical_critical_day'] = (phisical == 0)
    biorhythm['emotional_critical_day'] = (emotional == 0)
    biorhythm['intellectual_critical_day'] = (intellectual == 0)

    return biorhythm


def main():
    # create the updater, that will automatically create also a dispatcher and a queue to
    # make them dialogue
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher

    # add handlers for start and help commands
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    # add an handler for our biorhythm command
    dispatcher.add_handler(CommandHandler("biorhythm", biorhythm))

    # add an handler for normal text (not commands)
    dispatcher.add_handler(MessageHandler(Filters.text, text))

    # add an handler for errors
    dispatcher.add_error_handler(error)

    # start your shiny new bot
    updater.start_polling()

    # run the bot until Ctrl-C
    updater.idle()


if __name__ == '__main__':
    main()
