from unittest.mock import MagicMock, call

from app.api.command_list import CallbackId
from base.routing.dispatcher import Dispatcher
from base.routing.registration import CommandHandlerReg, CallbackHandlerReg, PendingRequestHandlerReg
from tests.utils import BaseTestCase
from tests.utils import MatcherAny


class TestDispatcher(BaseTestCase):
    def test_registration(self):
        updater_mock = MagicMock()

        Dispatcher(updater_mock, MagicMock(),
                   [
                       CommandHandlerReg(['command_1', 'command_2'], MagicMock()),
                       CallbackHandlerReg(CallbackId.COMMON_DELETE_MESSAGE, MagicMock()),
                       PendingRequestHandlerReg('test_request', MagicMock()),
                   ])
        updater_mock.dispatcher.add_handler.assert_has_calls(
            [call(MatcherAny()), call(MatcherAny()), call(MatcherAny())])

    def test_crash_on_bad_registration(self):
        with self.assertRaises(ValueError):
            Dispatcher(MagicMock(), MagicMock(), ["incorrect_Reg_object"])
