from unittest.mock import MagicMock, PropertyMock

from telegram import Chat, User as TgUser, Message as TgMessage

from base.database.scoped_session import ScopedSession
from base.handler.context.context import Context
from base.models.all import TelegramUser
from base.routing.pending_requests import PendingRequests, PendingRequestsDispatcher
from tests.utils import InBotTestCase


class TestPendingRequests(InBotTestCase):
    def test_create_and_get_request(self):
        with ScopedSession(self.connection) as session:
            session.add(TelegramUser(tg_id=1, first_name='a'))
        update = MagicMock()
        type(update).effective_user = TgUser(1, 'a', is_bot=False)
        type(update.effective_chat).type = PropertyMock(return_value=Chat.PRIVATE)
        with Context(update, MagicMock(), self.connection) as context:
            self.assertTrue(PendingRequests.create(context.session, 'test_request', context.sender, context.group))
        with Context(update, MagicMock(), self.connection) as context:
            self.assertEqual(PendingRequests.get(context.session, context.sender, context.group).type, 'test_request')

    def test_replace_request(self):
        with ScopedSession(self.connection) as session:
            session.add(TelegramUser(tg_id=1, first_name='a'))
        update = MagicMock()
        type(update).effective_user = TgUser(1, 'a', is_bot=False)
        type(update.effective_chat).type = PropertyMock(return_value=Chat.PRIVATE)
        with Context(update, MagicMock(), self.connection) as context:
            self.assertTrue(PendingRequests.create(context.session, 'test_request', context.sender, context.group))
        with Context(update, MagicMock(), self.connection) as context:
            PendingRequests.replace(context.session, 'new_test_request', context.sender, context.group)
        with Context(update, MagicMock(), self.connection) as context:
            self.assertEqual(PendingRequests.get(context.session, context.sender, context.group).type,
                             'new_test_request')

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
        type(update).message = TgMessage(000, MagicMock(), MagicMock(), text='test_message')

        disp = PendingRequestsDispatcher({})
        with Context(update, MagicMock(), self.connection) as context:
            disp.dispatch(context)

    def test_dispatching_no_handler(self):
        with ScopedSession(self.connection) as session:
            session.add(TelegramUser(tg_id=1, first_name='a'))
        update = MagicMock()
        type(update).effective_user = TgUser(1, 'a', is_bot=False)
        type(update.effective_chat).type = PropertyMock(return_value=Chat.PRIVATE)
        type(update).message = TgMessage(000, MagicMock(), MagicMock(), text='test_message')
        with Context(update, MagicMock(), self.connection) as context:
            self.assertTrue(PendingRequests.create(context.session, 'test_request', context.sender, context.group))

        disp = PendingRequestsDispatcher({})
        with Context(update, MagicMock(), self.connection) as context:
            disp.dispatch(context)

    def test_dispatching_duplicate_request(self):
        with ScopedSession(self.connection) as session:
            session.add(TelegramUser(tg_id=1, first_name='a'))
        update = MagicMock()
        type(update).effective_user = TgUser(1, 'a', is_bot=False)
        type(update.effective_chat).type = PropertyMock(return_value=Chat.PRIVATE)
        type(update).message = TgMessage(000, MagicMock(), MagicMock(), text='test_message')
        with Context(update, MagicMock(), self.connection) as context:
            self.assertTrue(PendingRequests.create(context.session, 'test_request', context.sender, context.group))
            self.assertFalse(PendingRequests.create(context.session, 'test_request', context.sender, context.group))

    def test_dispatching_ok(self):
        callable_fn = MagicMock()
        with ScopedSession(self.connection) as session:
            session.add(TelegramUser(tg_id=1, first_name='a'))
        update = MagicMock()
        type(update).effective_user = TgUser(1, 'a', is_bot=False)
        type(update.effective_chat).type = PropertyMock(return_value=Chat.PRIVATE)
        type(update).message = TgMessage(000, MagicMock(), MagicMock(), text='test_message')
        with Context(update, MagicMock(), self.connection) as context:
            self.assertTrue(PendingRequests.create(context.session, 'test_request', context.sender, context.group))

        disp = PendingRequestsDispatcher({'test_request': callable_fn})
        with Context(update, MagicMock(), self.connection) as context:
            disp.dispatch(context)
            callable_fn.assert_called_once_with(context)
