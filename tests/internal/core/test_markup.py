from unittest.mock import MagicMock, PropertyMock

from telegram import InlineKeyboardButton

from app.internal.core.markup.callback_commands import decode_callback_data, CallbackData
from app.internal.core.markup.inline_menu import InlineMenu
from tests.base import BaseTestCase


class TestInlineMenu(BaseTestCase):
    def test_callback_data(self):
        update = MagicMock()
        type(update.callback_query).data = PropertyMock(return_value='111:1:False What?')
        self.assertEqual(CallbackData('111', '1', ['False', 'What?']), decode_callback_data(update))
        type(update.callback_query).data = PropertyMock(return_value='111::False What?')
        self.assertEqual(CallbackData('111', '', ['False', 'What?']), decode_callback_data(update))

    def test_general(self):
        menu = InlineMenu([[('button', [111, 'test', 500])]])
        self.assertEqual([[InlineKeyboardButton('button', callback_data='111::test 500')]], menu.inline_keyboard)

    def test_user_id(self):
        menu = InlineMenu([[('button', [111, 'test', 500])]], user_tg_id=1234)
        self.assertEqual([[InlineKeyboardButton('button', callback_data='111:1234:test 500')]], menu.inline_keyboard)
