from unittest.mock import MagicMock, PropertyMock

from telegram import Chat, User as TgUser, Message as TgMessage

from app.api.command_list import PendingRequestId
from base.database.scoped_session import ScopedSession
from base.handler.wrapper.context import Context
from base.models.all import TelegramUser
from base.handler.wrapper.requests import Requests
from tests.utils import InBotTestCase


class TestRequests(InBotTestCase):
    def test_create_and_get_request(self):
        with ScopedSession(self.connection) as session:
            session.add(TelegramUser(tg_id=1, first_name='a'))
        update = MagicMock()
        type(update).effective_user = TgUser(1, 'a', is_bot=False)
        type(update.effective_chat).type = PropertyMock(return_value=Chat.PRIVATE)
        type(update.effective_message).message_id = 000
        with Context(update, MagicMock(), self.connection) as context:
            self.assertTrue(Requests.create(context, PendingRequestId.EXAMPLE_DUMMY_TYPE))
        with Context(update, MagicMock(), self.connection) as context:
            self.assertEqual(Requests.get(context).type, 'dummy')

    def test_replace_request(self):
        with ScopedSession(self.connection) as session:
            session.add(TelegramUser(tg_id=1, first_name='a'))
        update = MagicMock()
        type(update).effective_user = TgUser(1, 'a', is_bot=False)
        type(update.effective_chat).type = PropertyMock(return_value=Chat.PRIVATE)
        type(update.effective_message).message_id = 000
        with Context(update, MagicMock(), self.connection) as context:
            self.assertTrue(Requests.create(context, PendingRequestId.EXAMPLE_DUMMY_TYPE))
            old_id = Requests.get(context).id
        with Context(update, MagicMock(), self.connection) as context:
            Requests.replace(context, PendingRequestId.EXAMPLE_DUMMY_TYPE)
        with Context(update, MagicMock(), self.connection) as context:
            self.assertEqual(Requests.get(context).type, PendingRequestId.EXAMPLE_DUMMY_TYPE)
            self.assertNotEqual(old_id, Requests.get(context))

    def test_duplicate_request(self):
        with ScopedSession(self.connection) as session:
            session.add(TelegramUser(tg_id=1, first_name='a'))
        update = MagicMock()
        type(update).effective_user = TgUser(1, 'a', is_bot=False)
        type(update.effective_chat).type = PropertyMock(return_value=Chat.PRIVATE)
        type(update).effective_message = TgMessage(000, MagicMock(), MagicMock(), text='test_message')
        with Context(update, MagicMock(), self.connection) as context:
            self.assertTrue(Requests.create(context, PendingRequestId.EXAMPLE_DUMMY_TYPE))
            self.assertFalse(Requests.create(context, PendingRequestId.EXAMPLE_DUMMY_TYPE))
