from collections import namedtuple
from typing import List
from typing import Optional

from sqlalchemy import and_
from telegram import Update
from telegram.ext import CallbackContext

from base.database import SessionScope
from base.handler.helpers.actions import Actions
from base.handler.helpers.inline_menu import InlineMenu, InlineMenuButton
from base.handler.wrappers.message import Message
from base.models import TelegramUser, TelegramGroup, TelegramUserRequest
from base.models.helpers import ModelHelpers

RawContextData = namedtuple('RawData', ['update', 'callback_context'])


class Context:
    def __init__(self, raw_data: Optional[RawContextData] = None,
                 message: Optional[Message] = None,
                 sender: Optional[TelegramUser] = None,
                 group: Optional[TelegramGroup] = None,
                 request: Optional[TelegramUserRequest] = None):
        self.raw_data: Optional[RawContextData] = raw_data
        self.message: Optional[Message] = message
        self.sender: Optional[TelegramUser] = sender
        self.group: Optional[TelegramGroup] = group
        self.request: Optional[TelegramUserRequest] = request

        # Can be filled by handler
        self.callback_answer: Optional[str] = None

    @classmethod
    def from_update(cls, update: Update, callback_context: CallbackContext):
        sender = Context._get_sender(update)
        group = Context._get_group(update)
        request = Context._get_request(sender, group)
        return cls(raw_data=RawContextData(update, callback_context),
                   message=Message.from_update(update),
                   sender=sender, group=group, request=request)

    # Shortcuts
    def send_callback_answer(self, text: str):
        self.callback_answer = text

    def personal_menu(self, markup: List[List[InlineMenuButton]]) -> InlineMenu:
        return InlineMenu(markup, user_tg_id=self.sender.tg_id)

    def send_message(self, text: str, **kwargs):
        return Actions.send_message(text, chat_id=self.message.chat_id, **kwargs)

    def edit_message(self, new_message: str, **kwargs):
        return Actions.edit_message(new_message,
                                    chat_id=self.message.chat_id, message_id=self.message.message_id, **kwargs)

    def edit_markup(self, new_markup: object):
        return Actions.edit_markup(new_markup, chat_id=self.message.chat_id, message_id=self.message.message_id)

    def delete_message(self):
        return Actions.delete_message(chat_id=self.message.chat_id, message_id=self.message.message_id)

    # Private methods
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @staticmethod
    def _get_sender(update: Update) -> Optional[TelegramUser]:
        if update.effective_user is None:
            return None
        return ModelHelpers.get_from_tg_user(update.effective_user)

    @staticmethod
    def _get_group(update: Update) -> Optional[TelegramGroup]:
        if update.effective_chat is None:
            return None
        return ModelHelpers.get_from_tg_chat(update.effective_chat)

    @staticmethod
    def _get_request(user: Optional[TelegramUser], group: Optional[TelegramGroup]) -> Optional[TelegramUserRequest]:
        if user is None:
            return None
        group_id = None if group is None else group.id
        return SessionScope.session().query(TelegramUserRequest).filter(and_(
            TelegramUserRequest.telegram_user_id == user.id,
            TelegramUserRequest.telegram_group_id == group_id)).one_or_none()
