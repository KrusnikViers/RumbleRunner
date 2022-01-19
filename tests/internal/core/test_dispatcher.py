from unittest.mock import MagicMock, call

from app.internal.core.dispatcher import Dispatcher
from app.internal.core.handler.filters import FilterType
from app.internal.core.handler.registration import CommandHandlerReg, CallbackHandlerReg
from tests.base import BaseTestCase
from tests.base import MatcherAny


class TestDispatcher(BaseTestCase):
    def test_registration(self):
        updater_mock = MagicMock()
        db_mock = MagicMock()
        callable_mock = MagicMock()

        Dispatcher(updater_mock, db_mock,
                   [
                       CommandHandlerReg(['command_1', 'command_2'], callable_mock),
                       CallbackHandlerReg(111, callable_mock, [FilterType.PERSONAL_CALLBACK])
                   ],
                   {
                       'pending_action': callable_mock
                   })
        updater_mock.dispatcher.add_handler.assert_has_calls(
            [call(MatcherAny()), call(MatcherAny()), call(MatcherAny())])
