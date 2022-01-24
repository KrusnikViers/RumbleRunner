from unittest.mock import MagicMock

from app.api.command_list import PendingRequestId
from base.database.scoped_session import ScopedSession
from base.handler.default.canceling import delete_message, delete_message_and_pending_request
from base.models.all import TelegramUser
from base.handler.wrapper.requests import Requests
from tests.utils import InBotTestCase


class TestCancelingHandlers(InBotTestCase):
    def test_delete_message(self):
        context = MagicMock()
        delete_message(context)
        context.actions.delete_message.assert_called_once()

    def test_delete_pending_message(self):
        with ScopedSession(self.connection) as session:
            user = TelegramUser(tg_id=1, first_name='a')
            session.add(user)
            context = MagicMock()
            type(context).session = session
            type(context).sender = user
            type(context).group_id = None
            type(context.actions).msg_id = 000
            self.assertTrue(Requests.create(context, PendingRequestId.EXAMPLE_DUMMY_TYPE))
            self.assertIsNotNone(Requests.get(context))
        with ScopedSession(self.connection) as session:
            user = session.query(TelegramUser).first()
            context = MagicMock()
            type(context).session = session
            type(context).sender = user
            type(context).group_id = None
            type(context.actions).msg_id = 000
            delete_message_and_pending_request(context)

            session.commit()
            self.assertEqual(Requests.get(context), None)
            context.actions.delete_message.assert_called_once()
