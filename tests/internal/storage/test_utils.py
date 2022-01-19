from app.internal.storage.models.all import TelegramUser
from app.internal.storage.scoped_session import ScopedSession
from app.internal.storage.util import select_and_update_by_tg_id
from tests.base import InBotTestCase


class TestDBUtils(InBotTestCase):
    def test_select_and_update_by_tg_id(self):
        with ScopedSession(self.connection) as session:
            new_user = TelegramUser(tg_id=1, first_name='aaa')
            session.add(new_user)

        with ScopedSession(self.connection) as session:
            user_as_is = select_and_update_by_tg_id(session, TelegramUser, 1)
            self.assertEqual(user_as_is.tg_id, 1)
            self.assertEqual(user_as_is.first_name, 'aaa')
            self.assertEqual(user_as_is.last_name, None)

        with ScopedSession(self.connection) as session:
            user_updated = select_and_update_by_tg_id(session, TelegramUser, 1,
                                                      first_name='aaa_new', last_name='aaa_last')
            self.assertEqual(user_updated.tg_id, 1)
            self.assertEqual(user_updated.first_name, 'aaa_new')
            self.assertEqual(user_updated.last_name, 'aaa_last')
            self.assertEqual(select_and_update_by_tg_id(session, TelegramUser, 1).first_name, 'aaa_new')

        with ScopedSession(self.connection) as session:
            very_new_user = select_and_update_by_tg_id(session, TelegramUser, 15, first_name='aaa_new')
            self.assertEqual(very_new_user.tg_id, 15)
            self.assertEqual(very_new_user.first_name, 'aaa_new')
            self.assertEqual(very_new_user.last_name, None)
