from unittest.mock import MagicMock

from app.api import CallbackId
from base import Message, InlineMenuButton
from base.handler.wrappers.context import Context
from tests.utils import InBotTestCase


class TestContext(InBotTestCase):
    def test_shortcuts(self):
        context = Context(message=Message(chat_id=1111, message_id=2222))
        new_markup = MagicMock()

        context.send_message('message', reply_markup=new_markup)
        self.bot_mock.send_message.assert_called_once_with(text='message', chat_id=1111, reply_markup=new_markup)

        context.edit_message('new_message')
        self.bot_mock.edit_message_text.assert_called_once_with('new_message', chat_id=1111, message_id=2222)

        context.edit_markup(new_markup)
        self.bot_mock.edit_message_reply_markup.assert_called_once_with(reply_markup=new_markup,
                                                                        chat_id=1111, message_id=2222)

        context.delete_message()
        self.bot_mock.delete_message.assert_called_once_with(chat_id=1111, message_id=2222)

    def test_personal_menu(self):
        context = Context(message=Message(chat_id=1111, message_id=2222), sender=self.new_user())
        test_menu = context.personal_menu([[InlineMenuButton('Test', CallbackId.COMMON_DELETE_MESSAGE)]])
        self.assertEqual(test_menu.inline_keyboard[0][0].callback_data, '0:{}:'.format(context.sender.tg_id))
