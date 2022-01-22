from unittest.mock import MagicMock

from base.database.scoped_session import ScopedSession
from base.handler.default.canceling import delete_message, delete_message_and_pending_request
from base.models.all import TelegramUser
from tests.utils import InBotTestCase
from base.routing.pending_requests import PendingRequests


class TestCancelingHandlers(InBotTestCase):
    def test_delete_message(self):
        context = MagicMock()
        delete_message(context)
        context.actions.delete_message.assert_called_once()

    def test_delete_pending_message(self):
        with ScopedSession(self.connection) as session:
            user = TelegramUser(tg_id=1, first_name='a')
            session.add(user)
            self.assertTrue(PendingRequests.create(session, 'test_action', user, None))
        with ScopedSession(self.connection) as session:
            user = session.query(TelegramUser).first()
            context = MagicMock()
            type(context).session = session
            type(context).sender = user
            type(context).group = None
            delete_message_and_pending_request(context)

            session.commit()
            self.assertEqual(PendingRequests.get(session, user, None), None)
            context.actions.delete_message.assert_called_once()

