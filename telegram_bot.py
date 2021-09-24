from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Dispatcher
import logging
from token_petrovich import token

logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)
updater = None


def start(update, context):
    s = "Шаломчики! Как жизнь бандитская?"
    update.message.reply_text(s)


def repeater(update, context):
    if context.user_data[echo]:
        update.message.reply_text(update.message.text)


def echo(update, context):
    command = context.args[0].lower()
    if ("on" == command):
        context.user_data[echo] = True
        update.message.reply_text("Repeater Started")
    elif ("off" == command):
        context.user_data[echo] = False
        update.message.reply_text("Repeater Stopped")


def start_bot():
    global updater
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text, repeater))
    dispatcher.add_handler(CommandHandler('echo', echo))

    updater.start_polling()
    updater.idle()


start_bot()
