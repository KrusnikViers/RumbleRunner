from unittest.mock import MagicMock, PropertyMock

from telegram import Chat

from app.internal.core.handler.filters import Filter, FilterType
from tests.base import BaseTestCase


class TestInputFilters(BaseTestCase):
    def test_is_valid(self):
        update = MagicMock()

        type(update).effective_chat = PropertyMock(return_value=None)
        type(update.effective_user).is_bot = PropertyMock(return_value=False)
        self.assertFalse(Filter.apply([], update))

        type(update).effective_chat = PropertyMock(return_value=MagicMock())
        type(update.effective_chat).type = Chat.CHANNEL
        self.assertFalse(Filter.apply([], update))

        type(update.effective_chat).type = Chat.PRIVATE
        self.assertTrue(Filter.apply([FilterType.PRIVATE], update))
        self.assertTrue(Filter.apply([FilterType.PRIVATE, FilterType.CALLBACK], update))

        type(update.effective_chat).type = Chat.GROUP
        self.assertTrue(Filter.apply([FilterType.GROUP, FilterType.CALLBACK], update))

        type(update.effective_chat).type = Chat.SUPERGROUP
        self.assertTrue(Filter.apply([FilterType.GROUP], update))

        self.assertFalse(Filter.apply([FilterType.PERSONAL_CALLBACK], update))
        type(update).callback_query = PropertyMock(return_value=None)
        self.assertFalse(Filter.apply([FilterType.PERSONAL_CALLBACK], update))
        type(update.effective_user).id = PropertyMock(return_value=1234)
        type(update).callback_query = PropertyMock(return_value=MagicMock())
        type(update.callback_query).data = PropertyMock(return_value='command:1234:some other data')
        self.assertTrue(Filter.apply([FilterType.PERSONAL_CALLBACK], update))
        type(update.callback_query).data = PropertyMock(return_value='command:wrong:some other data')
        self.assertFalse(Filter.apply([FilterType.PERSONAL_CALLBACK], update))

    def test_ignore_bots(self):
        update = MagicMock()
        type(update.effective_chat).type = PropertyMock(return_value=Chat.GROUP)
        type(update.effective_user).is_bot = PropertyMock(return_value=True)
        self.assertFalse(Filter.apply([], update))

    def test_allow_incomplete_data(self):
        update = MagicMock()
        type(update).effective_chat = PropertyMock(return_value=None)
        type(update).effective_user = PropertyMock(return_value=None)
        self.assertTrue(Filter.apply([FilterType.ALLOW_INCOMPLETE_DATA], update))

    def test_all_filters_covered(self):
        filters = [x for x in Filter.__dict__.values() if isinstance(x, int)]
        for filter_value in filters:
            self.assertTrue(filter_value in Filter._CHECKS or filter_value == FilterType.ALLOW_INCOMPLETE_DATA)
