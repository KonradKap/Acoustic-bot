import logging

from telegram.ext import ConversationHandler
import telegram

from db import add_user, get_user, get_users, remove_user
from models import User
import messages
import secret


def requires_admin(fn):
    def wrapper(update, context):
        if update.effective_user.id == secret.admin_id:
            fn(update, context)
        else:
            context.bot.send_message(
                chat_id=update.message.chat_id,
                text=messages.insufficient_permissions)
    return wrapper


def on_error(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=messages.on_error)


def start(message):
    def wrapper(update, context):
        logging.debug("WRAPPER")
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=message)
    return wrapper


def register_start(update, context):
    if get_user(update.effective_user.id):
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=messages.already_registered.format(
                update.effective_user.username))
        return ConversationHandler.END

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=messages.password_request)
    return "waiting for password"


def received_password(update, context):
    password = update.message.text
    if password != secret.register_password:
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=messages.wrong_password)
    else:
        user = update.effective_user
        add_user(
            User(user.id, user.username, update.message.chat_id))
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=messages.successful_registration.format(user.username))
    return ConversationHandler.END


def cancel(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=messages.cancel)
    return ConversationHandler.END


def unregister(update, context):
    if not get_user(update.effective_user.id):
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=messages.not_registered)
    else:
        remove_user(update.effective_user.id)
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=messages.unregistered_message)


def register_status(update, context):
    result = bool(get_user(update.effective_user.id))
    reply_message = (
        messages.user_registered if result else messages.user_not_registered)
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=reply_message)


def message_start(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=messages.message_request,
        parse_mode=telegram.ParseMode.MARKDOWN)
    return 'waiting for message'


def received_message(to_who):
    def wrapper(update, context):
        try:
            sender = get_user(update.effective_user.id)
            receiver_chat_id = getattr(sender, to_who)
            context.bot.send_message(
                chat_id=receiver_chat_id,
                text=messages.got_message.format(
                    messages.who_to_alias(to_who)),
                parse_mode=telegram.ParseMode.MARKDOWN)
            context.bot.send_message(
                chat_id=receiver_chat_id,
                text=update.message.text)
        except (AttributeError, telegram.error.BadRequest) as error:
            logging.warning(
                f'{receiver_chat_id} got no message, error: {error}')
            context.bot.send_message(
                chat_id=sender.chat_id,
                text=messages.message_failed,
                parse_mode=telegram.ParseMode.MARKDOWN)
            return ConversationHandler.END

        context.bot.send_message(
            chat_id=sender.chat_id,
            text=messages.message_send,
            parse_mode=telegram.ParseMode.MARKDOWN)
        return ConversationHandler.END
    return wrapper


@requires_admin
def list_users(update, context):
    users = "\n".join(user.username for user in get_users())
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=f"Users \n{users}")
