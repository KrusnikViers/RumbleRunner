from base.database.session_scope import SessionScope
from base.models.all import TelegramUser
from tests.utils import BaseTestCase
from base.database.connection import DatabaseConnection


class TestScopedSession(BaseTestCase):
    def test_session_rollback(self):
        connection = DatabaseConnection.create_for_tests()
        with self.assertRaises(Exception):
            with SessionScope(connection) as session:
                new_user = TelegramUser(tg_id=0, first_name='test')
                session.add(new_user)
                self.assertEqual(1, len(session.query(TelegramUser).all()))
                session.flush()
                raise Exception

        # Make sure, that after exception inside session, session will be rolled back.
        with SessionScope(connection) as session:
            self.assertEqual(0, len(session.query(TelegramUser).all()))
