from telegram import Update
from telegram.ext import CallbackQueryHandler, CommandHandler, MessageHandler, \
    Updater, CallbackContext, \
    Filters as TgFilters

from app.internal.core.handler.context import Context
from app.internal.core.handler.filters import FilterType
from app.internal.core.handler.memberhsip import maybe_update_memberships
from app.internal.core.handler.pending_request import PendingRequestsDispatcher
from app.internal.core.handler.registration import CommandHandlerReg, CallbackHandlerReg, create_handler_callable
from app.internal.storage.connection import DatabaseConnection


class Dispatcher:
    def __init__(self, updater: Updater, db_connection: DatabaseConnection, general_handlers: list,
                 pending_requests_handlers: list):
        self.db = db_connection
        self.updater = updater
        self.pending_requests_dispatcher = PendingRequestsDispatcher(pending_requests_handlers)

        for handler in general_handlers:
            if isinstance(handler, CommandHandlerReg):
                handler_callable = create_handler_callable(handler.callable_fn,
                                                           Dispatcher._normalize_filters(handler.filters),
                                                           db_connection)
                final_handler = CommandHandler(handler.commands, handler_callable)
                updater.dispatcher.add_handler(final_handler)
            elif isinstance(handler, CallbackHandlerReg):
                handler_callable = create_handler_callable(handler.callable_fn,
                                                           Dispatcher._normalize_filters(handler.filters),
                                                           db_connection)
                final_handler = CallbackQueryHandler(handler_callable, pattern=handler.pattern)
                updater.dispatcher.add_handler(final_handler)
            else:
                assert False

        # universal_handler_callable = functools.partial(self._universal_handler, self)
        updater.dispatcher.add_handler(MessageHandler(TgFilters.all, self._universal_handler))

    def _universal_handler(self, update: Update, callback_context: CallbackContext):
        with Context(update, callback_context, self.db) as context:
            maybe_update_memberships(context)
            self.pending_requests_dispatcher.maybe_dispatch(context)

    @staticmethod
    def _normalize_filters(filters: list, for_callback: bool = False) -> list:
        if filters is None:
            filters = []
        if for_callback:
            filters += [FilterType.CALLBACK]
        return list(set(filters))
