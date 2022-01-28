from telegram import InlineKeyboardButton

from base import InlineMenu, InlineMenuButton
from tests.utils import BaseTestCase


class TestInlineMenu(BaseTestCase):
    def test_general(self):
        menu = InlineMenu([[InlineMenuButton('button', 111, 'test 500')]])
        self.assertEqual([[InlineKeyboardButton('button', callback_data='111::test 500')]], menu.inline_keyboard)

    def test_user_id(self):
        menu = InlineMenu([[InlineMenuButton('button', 111, 'test 500')]], user_tg_id=1234)
        self.assertEqual([[InlineKeyboardButton('button', callback_data='111:1234:test 500')]], menu.inline_keyboard)
