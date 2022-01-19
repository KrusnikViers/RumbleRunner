from telegram import TelegramError

from app.public.handlers import Context


def cancel_delete_message_callback(context: Context):
    try:
        context.update.callback_query.delete_message()
    except TelegramError:
        pass
