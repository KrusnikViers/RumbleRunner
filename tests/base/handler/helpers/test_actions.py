from telegram import TelegramError, Message as TgMessage, Chat

from unittest.mock import MagicMock
from base.handler.helpers.actions import Actions
from tests.utils import InBotTestCase


class TestContextActions(InBotTestCase):
    def test_functions(self):
        Actions.send_message('test', chat_id=111)
        self.bot_mock.send_message.assert_called_with(111, 'test')



