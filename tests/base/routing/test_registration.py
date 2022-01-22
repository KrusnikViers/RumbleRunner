from unittest.mock import MagicMock, PropertyMock

from base.handler.context.wrapper_functions import WrapperFunctions
from base.handler.default.reporting import ReportsSender
from tests.utils import InBotTestCase


class TestCallbackRegistration(InBotTestCase):
    def test_usual_handler(self):
        callable_fn = MagicMock()
        update = MagicMock()
        type(update).effective_chat = PropertyMock(return_value=None)
        type(update).effective_user = PropertyMock(return_value=None)
        WrapperFunctions.universal(callable_fn, self.connection, update, MagicMock())
        callable_fn.assert_called_once()

    def test_handler_raises_exception_no_global_crash(self):
        ReportsSender.instance = MagicMock()
        type(ReportsSender.instance).admin_username = PropertyMock(return_value=None)

        def callable_fn(_):
            raise ValueError

        update = MagicMock()
        type(update).effective_chat = PropertyMock(return_value=None)
        type(update).effective_user = PropertyMock(return_value=None)
        WrapperFunctions.universal(callable_fn, self.connection, update, MagicMock())
