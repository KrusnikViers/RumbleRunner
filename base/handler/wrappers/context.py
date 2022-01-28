from collections import namedtuple
from typing import Optional

from sqlalchemy import and_
from telegram import Update
from telegram.ext import CallbackContext
from base.handler.wrappers.bot_scope import BotScope
from base.database.session_scope import SessionScope
from base.handler.wrappers.message import Message
from base.models.all import TelegramUser, TelegramGroup, TelegramUserRequest
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

    @classmethod
    def from_update(cls, update: Update, callback_context: CallbackContext):
        sender = Context._get_sender(update)
        group = Context._get_group(update)
        request = Context._get_request(sender, group)
        return cls(raw_data=RawContextData(update, callback_context),
                   message=Message.from_update(update),
                   sender=sender, group=group, request=request)

    # Private methods
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.raw_data and self.raw_data.update.callback_query:
            BotScope.bot().answer_callback_query(self.raw_data.update.callback_query.id)

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
