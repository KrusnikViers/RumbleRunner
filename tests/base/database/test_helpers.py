from base import DBHelpers, SessionScope, TelegramUser
from tests.utils import InBotTestCase


class TestDBUtils(InBotTestCase):
    def test_select_and_update_by_tg_id(self):
        new_user = TelegramUser(tg_id=1, first_name='aaa')
        session = SessionScope.session()
        session.add(new_user)

        user_as_is = DBHelpers.select_and_update_by_tg_id(TelegramUser, 1)
        self.assertEqual(user_as_is.tg_id, 1)
        self.assertEqual(user_as_is.first_name, 'aaa')
        self.assertEqual(user_as_is.last_name, None)

        user_updated = DBHelpers.select_and_update_by_tg_id(TelegramUser, 1, first_name='aaa_new', last_name='aaa_last')
        self.assertEqual(user_updated.tg_id, 1)
        self.assertEqual(user_updated.first_name, 'aaa_new')
        self.assertEqual(user_updated.last_name, 'aaa_last')

        self.assertEqual(DBHelpers.select_and_update_by_tg_id(TelegramUser, 1).first_name, 'aaa_new')

        very_new_user = DBHelpers.select_and_update_by_tg_id(TelegramUser, 15, first_name='aaa_new')
        self.assertEqual(very_new_user.tg_id, 15)
        self.assertEqual(very_new_user.first_name, 'aaa_new')
        self.assertEqual(very_new_user.last_name, None)
