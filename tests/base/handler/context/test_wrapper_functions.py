from unittest.mock import MagicMock

from telegram import Chat, User as TgUser

from base.handler.context.definitions import ChatType
from base.handler.context.wrapper_functions import WrapperFunctions
from tests.utils import InBotTestCase


class TestWrapperFunctions(InBotTestCase):
    def test_command_called(self):
        update = MagicMock()
        type(update.effective_chat).type = Chat.PRIVATE
        type(update).effective_user = TgUser(id=11, first_name='a', is_bot=False)
        callable_fn = MagicMock()
        WrapperFunctions.command(callable_fn, ChatType.ALL, self.connection, update, MagicMock())
        callable_fn.assert_called_once()

    def test_callback_called(self):
        update = MagicMock()
        type(update.effective_chat).type = Chat.PRIVATE
        type(update).effective_user = TgUser(id=11, first_name='a', is_bot=False)
        type(update.callback_query).data = '1::'
        callable_fn = MagicMock()
        WrapperFunctions.callback(callable_fn, ChatType.ALL, self.connection, update, MagicMock())
        callable_fn.assert_called_once()

    def test_callback_called_personal(self):
        update = MagicMock()
        type(update.effective_chat).type = Chat.PRIVATE
        type(update).effective_user = TgUser(id=11, first_name='a', is_bot=False)
        type(update.callback_query).data = '1:11:'
        callable_fn = MagicMock()
        WrapperFunctions.callback(callable_fn, ChatType.ALL, self.connection, update, MagicMock())
        callable_fn.assert_called_once()

    def test_callback_wrong_user(self):
        update = MagicMock()
        type(update.effective_chat).type = Chat.PRIVATE
        type(update).effective_user = TgUser(id=11, first_name='a', is_bot=False)
        type(update.callback_query).data = '1:12:'
        callable_fn = MagicMock()
        WrapperFunctions.callback(callable_fn, ChatType.ALL, self.connection, update, MagicMock())
        callable_fn.assert_not_called()

    def test_command_wrong_chat_type(self):
        update = MagicMock()
        type(update.effective_chat).type = Chat.PRIVATE
        callable_fn = MagicMock()
        WrapperFunctions.command(callable_fn, ChatType.GROUP, self.connection, update, MagicMock())
        callable_fn.assert_not_called()
