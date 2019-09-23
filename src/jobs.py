from random import randrange
import logging

from telegram.ext import (
    CommandHandler, ConversationHandler, MessageHandler, Filters)
import telegram

from commands import start, message_start, received_message, cancel
from db import get_users, update_pair
import messages


def _generate_pairs(users):
    def shuffle(items):
        items = items[:]
        i = len(items)
        while i > 1:
            i = i - 1
            j = randrange(i)
            items[j], items[i] = items[i], items[j]
        return items

    takers = shuffle(users)
    return list(zip(users, takers))


def _add_handlers(updater):
    for group, handlers in updater.dispatcher.handlers.items():
        updater.dispatcher.handlers[group] = []
    updater.dispatcher.add_handler(CommandHandler(['start', 'help'],
                                                  start(messages.ss_help)))
    updater.dispatcher.add_handler(ConversationHandler(
        entry_points=[CommandHandler('ask', message_start)],
        states={
            'waiting for message': [
                MessageHandler(Filters.text,
                               received_message('giver_chat_id'))]
        },
        fallbacks=[CommandHandler('cancel', cancel)]))
    updater.dispatcher.add_handler(ConversationHandler(
        entry_points=[CommandHandler('reply', message_start)],
        states={
            'waiting for message': [
                MessageHandler(Filters.text,
                               received_message('taker_chat_id'))]
        },
        fallbacks=[CommandHandler('cancel', cancel)]))


def start_ss(context):
    updater = context.job.context

    pairing = _generate_pairs(get_users())
    for giver, taker in pairing:
        try:
            update_pair(giver, taker)
            context.bot.send_message(
                chat_id=giver.chat_id,
                text=messages.ss_started.format(taker.username)
                + messages.ss_help)
        except telegram.error.BadRequest as error:
            logging.warning(f'{giver} got no message, error: {error}')

    _add_handlers(updater)
