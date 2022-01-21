from base.handler.context.data import Data
from unittest.mock import MagicMock, PropertyMock
from telegram import Chat

from tests.utils import BaseTestCase

class TestContextData(BaseTestCase):
    def test_message_extraction(self):
        update = MagicMock()
        type(update).effective_user = PropertyMock(return_value=None)
        type(update.effective_chat).type = PropertyMock(return_value=Chat.PRIVATE)
        type(update.message).text = PropertyMock(return_value='/command some text after')

        data = Data(update)
        self.assertEqual(data.bot_command, '/command')
        self.assertEqual(data.text, 'some text after')
        self.assertFalse(data.is_empty)

    def test_empty_message_extraction(self):
        update = MagicMock()
        type(update).effective_user = PropertyMock(return_value=None)
        type(update.effective_chat).type = PropertyMock(return_value=Chat.PRIVATE)
        type(update.message).text = PropertyMock(return_value='/command_and_nothing_more')

        data = Data(update)
        self.assertEqual(data.bot_command, '/command_and_nothing_more')
        self.assertEqual(data.text, None)
        self.assertFalse(data.is_empty)
