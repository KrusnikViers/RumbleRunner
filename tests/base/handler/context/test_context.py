from unittest.mock import MagicMock, PropertyMock

from telegram import Chat

from base.handler.wrapper import context
from tests.utils import InBotTestCase


class TestContext(InBotTestCase):
    def test_callback_resolving(self):
        update = MagicMock()
        type(update).effective_user = PropertyMock(return_value=None)
        type(update.effective_chat).type = PropertyMock(return_value=Chat.PRIVATE)
        type(update).message = PropertyMock(return_value=None)
        instance = context.Context(update, MagicMock(), MagicMock())
        with instance:
            self.assertFalse(instance.update.callback_query.answer.called)
        self.assertTrue(instance.update.callback_query.answer.called)

