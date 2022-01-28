from unittest.mock import MagicMock

from telegram import TelegramError

from base.handler.helpers.actions import Actions
from tests.utils import InBotTestCase, MatcherAny


class TestContextActions(InBotTestCase):
    def test_ignore_exception(self):
        self.bot_mock.send_message.side_effect = TelegramError('random error')
        Actions.send_message('test', chat_id=111)

    def test_functions(self):
        Actions.send_message('test', chat_id=111)
        self.bot_mock.send_message.assert_called_with(111, 'test')

        Actions.edit_message('new_message', chat_id=111, message_id=222)
        self.bot_mock.edit_message_text.assert_called_once_with('new_message', chat_id=111, message_id=222)

        Actions.edit_markup(MagicMock(), chat_id=111, message_id=222)
        self.bot_mock.edit_message_text.assert_called_once_with(MatcherAny(), chat_id=111, message_id=222)
