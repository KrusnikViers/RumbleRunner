from unittest.mock import MagicMock, PropertyMock

from telegram import Chat, User as TgUser, Message as TgMessage

from app.routing.pending_requests import PendingRequestType
from base.database.scoped_session import ScopedSession
from base.handler.context.context import Context
from base.handler.context.definitions import ChatType
from base.handler.context.wrapper_functions import WrapperFunctions
from base.models.all import TelegramUser
from base.routing.pending_requests import PendingRequests
from tests.utils import InBotTestCase


class TestWrapperFunctions(InBotTestCase):
    def test_command_called(self):
        update = MagicMock()
        type(update.effective_chat).type = Chat.PRIVATE
        type(update).effective_user = TgUser(id=11, first_name='a', is_bot=False)
        callable_fn = MagicMock()
        WrapperFunctions.command(callable_fn, ChatType.ALL, self.connection, update, MagicMock())
        callable_fn.assert_called_once()

    def test_callback_called(self):
        update = MagicMock()
        type(update.effective_chat).type = Chat.PRIVATE
        type(update).effective_user = TgUser(id=11, first_name='a', is_bot=False)
        type(update.callback_query).data = '1::'
        callable_fn = MagicMock()
        WrapperFunctions.callback(callable_fn, ChatType.ALL, self.connection, update, MagicMock())
        callable_fn.assert_called_once()

    def test_callback_called_personal(self):
        update = MagicMock()
        type(update.effective_chat).type = Chat.PRIVATE
        type(update).effective_user = TgUser(id=11, first_name='a', is_bot=False)
        type(update.callback_query).data = '1:11:'
        callable_fn = MagicMock()
        WrapperFunctions.callback(callable_fn, ChatType.ALL, self.connection, update, MagicMock())
        callable_fn.assert_called_once()

    def test_callback_wrong_user(self):
        update = MagicMock()
        type(update.effective_chat).type = Chat.PRIVATE
        type(update).effective_user = TgUser(id=11, first_name='a', is_bot=False)
        type(update.callback_query).data = '1:12:'
        callable_fn = MagicMock()
        WrapperFunctions.callback(callable_fn, ChatType.ALL, self.connection, update, MagicMock())
        callable_fn.assert_not_called()

    def test_command_wrong_chat_type(self):
        update = MagicMock()
        type(update.effective_chat).type = Chat.PRIVATE
        callable_fn = MagicMock()
        WrapperFunctions.command(callable_fn, ChatType.GROUP, self.connection, update, MagicMock())
        callable_fn.assert_not_called()


class TestPendingRequestsDispatching(InBotTestCase):
    def test_dispatching_no_sender(self):
        WrapperFunctions.pending_action({}, self.connection, MagicMock(), MagicMock())

    def test_dispatching_no_request(self):
        with ScopedSession(self.connection) as session:
            session.add(TelegramUser(tg_id=1, first_name='a'))
        update = MagicMock()
        type(update).effective_user = TgUser(1, 'a', is_bot=False)
        type(update.effective_chat).type = PropertyMock(return_value=Chat.PRIVATE)
        type(update).message = TgMessage(000, MagicMock(), MagicMock(), text='test_message')
        WrapperFunctions.pending_action({}, self.connection, update, MagicMock())

    def test_dispatching_no_handler(self):
        with ScopedSession(self.connection) as session:
            session.add(TelegramUser(tg_id=1, first_name='a'))
        update = MagicMock()
        type(update).effective_user = TgUser(1, 'a', is_bot=False)
        type(update.effective_chat).type = PropertyMock(return_value=Chat.PRIVATE)
        type(update).message = TgMessage(000, MagicMock(), MagicMock(), text='test_message')
        with Context(update, MagicMock(), self.connection) as context:
            self.assertTrue(PendingRequests.create(context, PendingRequestType.EXAMPLE_DUMMY_TYPE))
        WrapperFunctions.pending_action({}, self.connection, update, MagicMock())

    def test_dispatching_ok(self):
        callable_fn = MagicMock()
        with ScopedSession(self.connection) as session:
            session.add(TelegramUser(tg_id=1, first_name='a'))
        update = MagicMock()
        type(update).effective_user = TgUser(1, 'a', is_bot=False)
        type(update.effective_chat).type = PropertyMock(return_value=Chat.PRIVATE)
        type(update).message = TgMessage(000, MagicMock(), MagicMock(), text='test_message')
        with Context(update, MagicMock(), self.connection) as context:
            self.assertTrue(PendingRequests.create(context, PendingRequestType.EXAMPLE_DUMMY_TYPE))

        WrapperFunctions.pending_action({PendingRequestType.EXAMPLE_DUMMY_TYPE: callable_fn},
                                        self.connection, update, MagicMock())
        callable_fn.assert_called_once()
