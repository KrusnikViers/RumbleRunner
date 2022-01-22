from collections import namedtuple
from typing import Optional

from telegram import Chat
from telegram import Update
from telegram.ext import CallbackContext

from base.database.connection import DatabaseConnection
from base.database.helpers import DBHelpers
from base.database.scoped_session import ScopedSession
from base.handler.context.actions import Actions
from base.handler.context.data import Data
from base.models.all import TelegramUser, TelegramGroup, TelegramUserRequest

RawContextData = namedtuple('RawData', ['update', 'callback_context'])


class Context(ScopedSession):
    def __init__(self, update: Update, callback_context: CallbackContext, db: DatabaseConnection):
        super(Context, self).__init__(db)
        self.update = update
        self.raw_data = RawContextData(update, callback_context)
        self.data = Data(update)
        self.actions = Actions(update)

        self.sender: Optional[TelegramUser] = None
        if update.effective_user is not None and not update.effective_user.is_bot:
            self.sender = DBHelpers.select_and_update_by_tg_id(self.session, TelegramUser, update.effective_user.id,
                                                               first_name=update.effective_user.first_name,
                                                               last_name=update.effective_user.last_name,
                                                               username=update.effective_user.username)
        self.group: Optional[TelegramGroup] = None
        if update.effective_chat and update.effective_chat.type in [Chat.GROUP, Chat.SUPERGROUP]:
            self.group = DBHelpers.select_and_update_by_tg_id(self.session, TelegramGroup, update.effective_chat.id,
                                                              name=update.effective_chat.title)

        self.pending_request: Optional[TelegramUserRequest] = None  # Set by dispatch_pending_requests handler

    def __enter__(self):
        super(Context, self).__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.update.callback_query:
            self.update.callback_query.answer()
        super(Context, self).__exit__(exc_type, exc_val, exc_tb)
