from unittest.mock import MagicMock, PropertyMock

from telegram import Chat, Update, Message as TgMessage

from app.api.command_list import CallbackId
from base.handler.wrappers.message import Message, CallbackData
from tests.utils import BaseTestCase


class TestMessage(BaseTestCase):
    def test_callback_data(self):
        data = CallbackData.parse('0:1:False What?')
        self.assertEqual(data.command, CallbackId.COMMON_DELETE_MESSAGE)
        self.assertEqual(data.user_id, 1)
        self.assertEqual(data.data, 'False What?')

        data = CallbackData.parse('0::')
        self.assertEqual(data.command, CallbackId.COMMON_DELETE_MESSAGE)
        self.assertIsNone(data.user_id)
        self.assertIsNone(data.data)

    def test_callback_data_encode(self):
        self.assertEqual(CallbackData(CallbackId.COMMON_DELETE_MESSAGE, data=['a', 14]).encode(), '0::a 14')
        self.assertEqual(CallbackData(CallbackId.COMMON_DELETE_MESSAGE, user_id=132, data=None).encode(), '0:132:')
        self.assertEqual(CallbackData(CallbackId.COMMON_DELETE_MESSAGE, user_id=11, data='a b').encode(), '0:11:a b')

    def test_message_extraction(self):
        update = Update(000, message=TgMessage(111, None, text='/command some text after', chat=Chat(222, Chat.PRIVATE)))
        message = Message.from_update(update)
        self.assertEqual(message.command, '/command')
        self.assertEqual(message.data, 'some text after')

    def test_empty_message_extraction(self):
        update = Update(000,
                        message=TgMessage(111, None, text='/command_only', chat=Chat(222, Chat.PRIVATE)))
        message = Message.from_update(update)
        self.assertEqual(message.command, '/command_only')
        self.assertIsNone(message.data)

    def test_usual_message_extraction(self):
        update = Update(000, message=TgMessage(111, None, text='  usual text ', chat=Chat(222, Chat.PRIVATE)))
        message = Message.from_update(update)
        self.assertIsNone(message.command)
        self.assertEqual(message.data, 'usual text')
