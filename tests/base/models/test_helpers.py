from telegram import User as TgUser

from base.models.helpers import ModelHelpers
from tests.utils import BaseTestCase


class TestModelHelpers(BaseTestCase):
    def test_user_from_bot(self):
        user = TgUser(333, 'definitely_not_bot', is_bot=True)
        # Make sure, that it does not even attempt to access query session.
        self.assertIsNone(ModelHelpers.get_from_tg_user(user))
