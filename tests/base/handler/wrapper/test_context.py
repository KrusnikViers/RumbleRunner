from unittest.mock import MagicMock, PropertyMock

from telegram import Chat, Update

from base.handler.wrappers import context
from tests.utils import InBotTestCase


class TestContext(InBotTestCase):
    def test_callback_resolving(self):
        instance = context.Context.from_update(MagicMock(), MagicMock())
        with instance:
            self.bot_mock.answer_callback_query.assert_not_called()
        self.bot_mock.answer_callback_query.assert_called_once()

