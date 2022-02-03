import functools
import logging
from typing import Optional

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
        def wrapper(*args, **kwargs):
            scope = _TelegramErrorsCatchScope()
            with scope:
                result = func(*args, **kwargs)
            if scope.was_interrupted:
                return None
            return result

        return wrapper


class Actions:
    @staticmethod
    @_TelegramErrorsCatchScope.return_status
    def send_message(text, chat_id: int, **kwargs):
        return BotScope.bot().send_message(chat_id=chat_id, text=text, **kwargs)

    @staticmethod
    @_TelegramErrorsCatchScope.return_status
    def edit_message(new_message: str, chat_id: int, message_id: int, **kwargs):
        return BotScope.bot().edit_message_text(new_message, chat_id=chat_id, message_id=message_id, **kwargs)

    @staticmethod
    @_TelegramErrorsCatchScope.return_status
    def edit_markup(new_markup, chat_id: int, message_id: int):
        return BotScope.bot().edit_message_reply_markup(reply_markup=new_markup, chat_id=chat_id, message_id=message_id)

    @staticmethod
    @_TelegramErrorsCatchScope.return_status
    def delete_message(chat_id: int, message_id: int):
        return BotScope.bot().delete_message(chat_id=chat_id, message_id=message_id)

    @staticmethod
    @_TelegramErrorsCatchScope.return_status
    def answer_callback(callback_query_id, text: Optional[str] = None):
        return BotScope.bot().answer_callback_query(callback_query_id, text=text)
