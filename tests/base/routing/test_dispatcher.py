from unittest.mock import MagicMock, call

from app.internal.core.dispatcher import Dispatcher
from app.internal.core.handler.filters import FilterType
from app.internal.core.handler.registration import CommandHandlerReg, CallbackHandlerReg
from tests.utils import BaseTestCase
from tests.utils import MatcherAny


class TestDispatcher(BaseTestCase):
    def test_registration(self):
        updater_mock = MagicMock()

        Dispatcher(updater_mock, MagicMock(),
                   [
                       CommandHandlerReg(['command_1', 'command_2'], MagicMock()),
                       CallbackHandlerReg(111, MagicMock(), [FilterType.PERSONAL_CALLBACK])
                   ],
                   {
                       'pending_action': MagicMock()
                   })
        updater_mock.dispatcher.add_handler.assert_has_calls(
            [call(MatcherAny()), call(MatcherAny()), call(MatcherAny())])

    def test_crash_on_bad_registration(self):
        with self.assertRaises(ValueError):
            Dispatcher(MagicMock(), MagicMock(), ["incorrect_Reg_object"], {})
