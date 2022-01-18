from typing import Optional

from telegram import Chat
from telegram import Message, Update
from telegram.ext import CallbackContext

from app.internal.storage.connection import DatabaseConnection
from app.internal.storage.models.all import TelegramGroup, TelegramUser, TelegramUserRequest
from app.internal.storage.scoped_session import ScopedSession
from app.internal.storage.util import select_and_update_by_tg_id


class Context(ScopedSession):
    def __init__(self, update: Update, callback_context: CallbackContext, db: DatabaseConnection):
        super(Context, self).__init__(db)
        self.update: Update = update
        self.callback_context: CallbackContext = callback_context
        self.sender: Optional[TelegramUser] = None
        self.pending_request: Optional[TelegramUserRequest] = None  # Set by dispatch_pending_requests handler
        if update.effective_user is not None and not update.effective_user.is_bot:
            self.sender = select_and_update_by_tg_id(self.session, TelegramUser, update.effective_user.id,
                                                     first_name=update.effective_user.first_name,
                                                     last_name=update.effective_user.last_name,
                                                     username=update.effective_user.username)
        self.group: Optional[TelegramGroup] = None
        if update.effective_chat.type in [Chat.GROUP, Chat.SUPERGROUP]:
            self.group = select_and_update_by_tg_id(self.session, TelegramGroup, update.effective_chat.id)

    def send_response_message(self, text, **kwargs) -> Message:
        return self.update.effective_chat.send_message(text, **kwargs)

    def command_arguments(self) -> str:
        call_text = self.update.message.text
        divider_index = call_text.find(' ')
        if divider_index == -1:
            return ''
        return call_text[divider_index + 1:].strip()

    def __enter__(self):
        super(Context, self).__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.update.callback_query:
            self.update.callback_query.answer()
        super(Context, self).__exit__(exc_type, exc_val, exc_tb)
