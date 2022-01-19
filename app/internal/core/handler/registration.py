import functools

from telegram import Update
from telegram.ext import CallbackContext

from app.internal.core.handler.context import Context
from app.internal.core.handler.filters import Filter
from app.internal.core.handler.reporting import ReportsSender
from app.internal.storage.connection import DatabaseConnection
from app.internal.storage.scoped_session import ScopedSession


# callable_fn signature: fn(context: Context)
class CommandHandlerReg:
    def __init__(self, commands: list, callable_fn, filters: list = None):
        self.commands = commands
        self.callable_fn = callable_fn
        self.filters = filters


# callable_fn signature: fn(context: Context)
# CALLBACK filter auto-applied for the instances of CallbackHandlerReg.
class CallbackHandlerReg:
    def __init__(self, callback_id: int, callable_fn, filters: list = None):
        self.pattern = '^{0}.*$'.format(str(callback_id))
        self.callable_fn = callable_fn
        self.filters = filters


def create_handler_callable(raw_callable, filters: list, db: DatabaseConnection):
    def _common_handler_callable(handler_callable, input_filters: list,  # predefined arguments
                                 update: Update, callback_context: CallbackContext):
        try:
            if Filter.apply(input_filters, update):
                with Context(update, callback_context, db) as context:
                    handler_callable(context)
        except Exception as e:
            with ScopedSession(db) as session:
                ReportsSender.report_exception(update, session)

    return functools.partial(_common_handler_callable, raw_callable, filters)
