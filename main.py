import logging
import os
from dotenv import load_dotenv

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
# For type annotations
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext

from vk import get_latest_news


load_dotenv()
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(funcName)s - %(levelname)s - %(message)s')


def start(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help_command(update: Update, context: CallbackContext):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def resend(update: Update, context: CallbackContext):
    """
    Resend wall posts to TG
    :param update:
    :param context: context.args[0] - count
    :return:
    """
    if not context.args:
        count = 3
    else:
        count = context.args[0]
    posts = get_latest_news(count=count)
    for post in posts:
        update.message.reply_text(post.text)


if __name__ == '__main__':
    logging.info('Application startup')
    logging.info('Loading token')
    updater = Updater(token=os.environ.get('TG_TOKEN'), use_context=True)
    dp = updater.dispatcher

    logging.info('Registering handlers')
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help_command))
    dp.add_handler(CommandHandler('resend', resend))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    logging.info('Starting polling')
    updater.start_polling()
    updater.idle()
