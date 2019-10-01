import logging
import datetime

from telegram.ext import (
    Updater, CommandHandler, ConversationHandler, MessageHandler, Filters)

from commands import (start, register_start, received_password, cancel,
                      unregister, register_status, list_users)
from jobs import start_ss
import secret
import messages


DAY_X = datetime.datetime(
    year=2019,
    month=10,
    day=1,
    hour=12)


def main():
    logging.basicConfig(
        format="[%(asctime)s] [%(levelname)s] [%(name)s] "
               "[%(funcName)s():%(lineno)s] [PID:%(process)d TID:%(thread)d] "
               "%(message)s",
        level=logging.DEBUG)
    updater = Updater(token=secret.token, use_context=True)
    # updater.dispatcher.add_error_handler(on_error)
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
    updater.dispatcher.add_handler(CommandHandler('shrug',
                                                  start(messages.shrug)))

    # updater.job_queue.run_once(
    #     start_ss,
    #     datetime.datetime.now() + datetime.timedelta(seconds=2),
    #     context=updater)
    updater.job_queue.run_once(start_ss, DAY_X, context=updater)
    updater.start_polling()


if __name__ == '__main__':
    main()
