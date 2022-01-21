from unittest.mock import MagicMock, PropertyMock

from app.internal.core.handler.filters import FilterType
from app.internal.core.handler.registration import create_handler_callable
from app.internal.core.handler.reporting import ReportsSender
from tests.utils import InBotTestCase


class TestCallbackRegistration(InBotTestCase):
    def test_usual_handler(self):
        callable_fn = MagicMock()
        wrapped_fn = create_handler_callable(callable_fn, [FilterType.ALLOW_INCOMPLETE_DATA], self.connection)
        update = MagicMock()
        type(update).effective_chat = PropertyMock(return_value=None)
        type(update).effective_user = PropertyMock(return_value=None)
        context = MagicMock()
        wrapped_fn(update, context)
        callable_fn.assert_called_once()

    def test_handler_raises_exception_no_global_crash(self):
        ReportsSender.instance = MagicMock()
        type(ReportsSender.instance).admin_username = PropertyMock(return_value=None)

        def callable_fn(_):
            raise ValueError

        wrapped_fn = create_handler_callable(callable_fn, [FilterType.ALLOW_INCOMPLETE_DATA], self.connection)
        update = MagicMock()
        type(update).effective_chat = PropertyMock(return_value=None)
        type(update).effective_user = PropertyMock(return_value=None)
        context = MagicMock()
        wrapped_fn(update, context)
