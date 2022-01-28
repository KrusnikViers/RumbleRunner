import functools
import logging

from telegram import TelegramError

from base.handler.wrappers.bot_scope import BotScope


class _TelegramErrorsCatchScope:
    def __init__(self):
        self.was_interrupted = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if isinstance(exc_val, TelegramError):
            logging.warning("Telegram returned error: {}".format(exc_val))
            self.was_interrupted = True
            return True

    @staticmethod
    def return_status(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> bool:
            scope = _TelegramErrorsCatchScope()
            with scope:
                func(*args, **kwargs)
            return not scope.was_interrupted

        return wrapper


class Actions:
    @staticmethod
    @_TelegramErrorsCatchScope.return_status
    def send_message(text, chat_id: int, **kwargs):
        BotScope.bot().send_message(chat_id=chat_id, text=text, **kwargs)

    @staticmethod
    @_TelegramErrorsCatchScope.return_status
    def edit_message(new_message: str, chat_id: int, message_id: int):
        BotScope.bot().edit_message_text(new_message, chat_id=chat_id, message_id=message_id)

    @staticmethod
    @_TelegramErrorsCatchScope.return_status
    def edit_markup(new_markup, chat_id: int, message_id: int):
        BotScope.bot().edit_message_reply_markup(reply_markup=new_markup, chat_id=chat_id, message_id=message_id)

    @staticmethod
    @_TelegramErrorsCatchScope.return_status
    def delete_message(chat_id: int, message_id: int):
        BotScope.bot().delete_message(chat_id=chat_id, message_id=message_id)
