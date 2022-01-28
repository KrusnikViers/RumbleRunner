import logging
from typing import Optional

from telegram import TelegramError

from base.handler.wrappers.bot_scope import BotScope
from base.handler.wrappers.message import Message


class _ScopedIgnoreTelegramErrors:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if isinstance(exc_val, TelegramError):
            logging.warning("Telegram returned error: {}".format(exc_val))
            return True


class Actions:
    @staticmethod
    def send_message(text, message: Optional[Message] = None, chat_id: Optional[int] = None, **kwargs):
        effective_chat_id = chat_id if chat_id is not None else message.chat_id
        with _ScopedIgnoreTelegramErrors():
            BotScope.bot().send_message(effective_chat_id, text, **kwargs)

    @staticmethod
    def edit_message(new_message: str, message: Optional[Message] = None,
                     chat_id: Optional[int] = None, message_id: Optional[int] = None):
        effective_chat_id = chat_id if chat_id is not None else message.chat_id
        effective_message_id = message_id if message_id is not None else message.message_id
        with _ScopedIgnoreTelegramErrors():
            BotScope.bot().edit_message_text(new_message,
                                             chat_id=effective_chat_id, message_id=effective_message_id)

    @staticmethod
    def edit_markup(new_markup, saved_msg_id=None, message: Optional[Message] = None,
                    chat_id: Optional[int] = None, message_id: Optional[int] = None):
        effective_chat_id = chat_id if chat_id is not None else message.chat_id
        effective_message_id = message_id if message_id is not None else message.message_id
        with _ScopedIgnoreTelegramErrors():
            BotScope.bot().edit_message_reply_markup(reply_markup=new_markup,
                                                     chat_id=effective_chat_id,
                                                     message_id=effective_message_id)

    @staticmethod
    def delete_message(message: Optional[Message] = None,
                       chat_id: Optional[int] = None, message_id: Optional[int] = None):
        effective_chat_id = chat_id if chat_id is not None else message.chat_id
        effective_message_id = message_id if message_id is not None else message.message_id
        with _ScopedIgnoreTelegramErrors():
            BotScope.bot().delete_message(chat_id=effective_chat_id, message_id=effective_message_id)
