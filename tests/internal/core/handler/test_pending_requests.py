from unittest.mock import MagicMock, PropertyMock

from telegram import Chat, User as TgUser

from app.internal.core.handler.pending_request import *
from app.internal.storage.models.all import TelegramUser
from app.internal.storage.scoped_session import ScopedSession
from tests.base import InBotTestCase


class TestPendingRequests(InBotTestCase):
    def test_create_and_get_request(self):
        with ScopedSession(self.connection) as session:
            session.add(TelegramUser(tg_id=1, first_name='a'))
        update = MagicMock()
        type(update).effective_user = TgUser(1, 'a', is_bot=False)
        type(update.effective_chat).type = PropertyMock(return_value=Chat.PRIVATE)
        with Context(update, MagicMock(), self.connection) as context:
            try_create_pending_request(context, 'test_request')
        with Context(update, MagicMock(), self.connection) as context:
            self.assertEqual(get_pending_request(context).type, 'test_request')

    def test_dispatching_no_sender(self):
        disp = PendingRequestsDispatcher({})
        with Context(MagicMock(), MagicMock(), self.connection) as context:
            disp.dispatch(context)

    def test_dispatching_no_request(self):
        with ScopedSession(self.connection) as session:
            session.add(TelegramUser(tg_id=1, first_name='a'))
        update = MagicMock()
        type(update).effective_user = TgUser(1, 'a', is_bot=False)
        type(update.effective_chat).type = PropertyMock(return_value=Chat.PRIVATE)
        type(update).message = 'test_message'

        disp = PendingRequestsDispatcher({})
        with Context(update, MagicMock(), self.connection) as context:
            disp.dispatch(context)

    def test_dispatching_no_handler(self):
        with ScopedSession(self.connection) as session:
            session.add(TelegramUser(tg_id=1, first_name='a'))
        update = MagicMock()
        type(update).effective_user = TgUser(1, 'a', is_bot=False)
        type(update.effective_chat).type = PropertyMock(return_value=Chat.PRIVATE)
        type(update).message = 'test_message'
        with Context(update, MagicMock(), self.connection) as context:
            try_create_pending_request(context, 'test_request')

        disp = PendingRequestsDispatcher({})
        with Context(update, MagicMock(), self.connection) as context:
            disp.dispatch(context)

    def test_dispatching_ok(self):
        callable_fn = MagicMock()
        with ScopedSession(self.connection) as session:
            session.add(TelegramUser(tg_id=1, first_name='a'))
        update = MagicMock()
        type(update).effective_user = TgUser(1, 'a', is_bot=False)
        type(update.effective_chat).type = PropertyMock(return_value=Chat.PRIVATE)
        type(update).message = 'test_message'
        with Context(update, MagicMock(), self.connection) as context:
            try_create_pending_request(context, 'test_request')

        disp = PendingRequestsDispatcher({'test_request': callable_fn})
        with Context(update, MagicMock(), self.connection) as context:
            disp.dispatch(context)
            callable_fn.assert_called_once_with(context)
