from typing import Optional

from telegram import Update, Bot, Message, TelegramError


class ScopedIgnoreTelegramErrors:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type == TelegramError:
            return True


class Actions:
    def __init__(self, update: Update):
        self.update: Update = update

        self.is_functional: bool = False
        self.bot: Optional[Bot] = None
        self.chat_id: Optional[int] = None
        self.msg_id: Optional[int] = None

        if self.update.effective_message:
            self._parse_message(self.update.effective_message)
        elif self.update.callback_query is not None and self.update.callback_query.message is not None:
            self._parse_message(self.update.callback_query.message)

    def _parse_message(self, message: Message):
        if message is not None:
            self.bot = message.bot
            self.chat_id = message.chat_id
            self.msg_id = message.message_id
            self.is_functional = True

    def send_message(self, text, **kwargs):
        with ScopedIgnoreTelegramErrors():
            self.bot.send_message(self.chat_id, text, **kwargs)

    def edit_message(self, new_text: str):
        with ScopedIgnoreTelegramErrors():
            self.bot.edit_message_text(new_text, chat_id=self.chat_id, message_id=self.msg_id)

    def edit_markup(self, new_markup):
        with ScopedIgnoreTelegramErrors():
            self.bot.edit_message_reply_markup(chat_id=self.chat_id, message_id=self.msg_id, reply_markup=new_markup)

    def delete_message(self):
        with ScopedIgnoreTelegramErrors():
            self.bot.delete_message(chat_id=self.chat_id, message_id=self.msg_id)
