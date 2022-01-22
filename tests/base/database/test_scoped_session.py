from base.database.scoped_session import ScopedSession
from base.models.all import TelegramUser
from tests.utils import InBotTestCase


class TestScopedSession(InBotTestCase):
    def test_session_rollback(self):
        with self.assertRaises(Exception):
            with ScopedSession(self.connection) as session:
                new_user = TelegramUser(tg_id=0, first_name='test')
                session.add(new_user)
                self.assertEqual(1, len(session.query(TelegramUser).all()))
                session.flush()
                raise Exception

        # Make sure, that after exception inside session, session will be rolled back.
        with ScopedSession(self.connection) as session:
            self.assertEqual(0, len(session.query(TelegramUser).all()))
