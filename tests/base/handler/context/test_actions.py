from telegram import TelegramError, Message, Chat

from unittest.mock import MagicMock
from base.handler.wrapper.actions import Actions, ScopedIgnoreTelegramErrors
from tests.utils import BaseTestCase


class TestContextActions(BaseTestCase):
    def test_scoped_errors_catch(self):
        with ScopedIgnoreTelegramErrors():
            raise TelegramError('msg')

    def test_functions(self):
        update = MagicMock()
        bot = MagicMock()
        type(update).effective_message = Message(000, MagicMock(), Chat(111, type=Chat.GROUP), bot=bot)
        action_set = Actions(update)

        action_set.edit_message('new_text')
        bot.edit_message_text.assert_called_with('new_text', chat_id=111, message_id=000)
        action_set.edit_markup(None)
        bot.edit_message_reply_markup.assert_called_with(chat_id=111, message_id=000, reply_markup=None)
        action_set.delete_message()
        bot.delete_message.assert_called_with(chat_id=111, message_id=000)


