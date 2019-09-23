import logging
import datetime

from telegram.ext import (
    Updater, CommandHandler, ConversationHandler, MessageHandler, Filters)

from commands import (start, register_start, received_password, cancel,
                      unregister, register_status, list_users)
from jobs import start_ss
import secret
import messages


def main():
    logging.basicConfig(
        format="[%(asctime)s] [%(levelname)s] [%(name)s] "
               "[%(funcName)s():%(lineno)s] [PID:%(process)d TID:%(thread)d] "
               "%(message)s",
        level=logging.DEBUG)
    updater = Updater(token=secret.token, use_context=True)
    updater.dispatcher.add_handler(CommandHandler(['start', 'help'],
                                                  start(messages.start)))
    updater.dispatcher.add_handler(ConversationHandler(
        entry_points=[CommandHandler('register', register_start)],
        states={
            "waiting for password": [MessageHandler(Filters.text,
                                                    received_password)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]))
    updater.dispatcher.add_handler(CommandHandler('unregister', unregister))
    updater.dispatcher.add_handler(CommandHandler('status',
                                                  register_status))

    updater.dispatcher.add_handler(CommandHandler('list_users', list_users))

    # updater.job_queue.run_once(start_ss, DAY_X, context=updater)
    updater.job_queue.run_once(
        start_ss,
        datetime.datetime.now() + datetime.timedelta(seconds=5),
        context=updater)
    updater.start_polling()


if __name__ == '__main__':
    main()
