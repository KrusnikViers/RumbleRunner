from telegram.ext import CallbackQueryHandler, CommandHandler, MessageHandler, \
    Updater, Filters as TgFilters

from app.internal.core.handler.filters import FilterType
from app.internal.core.handler.memberhsip import update_memberships
from app.internal.core.handler.pending_request import PendingRequestsDispatcher
from app.internal.core.handler.registration import CommandHandlerReg, CallbackHandlerReg, create_handler_callable
from app.internal.storage.connection import DatabaseConnection


class Dispatcher:
    def __init__(self, updater: Updater, db_connection: DatabaseConnection,
                 general_handlers: list, pending_requests_handlers: dict):
        self.db = db_connection
        self.updater = updater
        self.pending_requests_dispatcher = PendingRequestsDispatcher(pending_requests_handlers)

        self._add_default_handlers()
        self._add_custom_handlers(general_handlers)

    def _add_custom_handlers(self, custom_handlers: list):
        for handler in custom_handlers:
            if isinstance(handler, CommandHandlerReg):
                handler_callable = create_handler_callable(handler.callable_fn,
                                                           Dispatcher._normalize_filters(handler.filters),
                                                           self.db)
                final_handler = CommandHandler(handler.commands, handler_callable)
                self.updater.dispatcher.add_handler(final_handler)
            elif isinstance(handler, CallbackHandlerReg):
                handler_callable = create_handler_callable(handler.callable_fn,
                                                           Dispatcher._normalize_filters(handler.filters,
                                                                                         for_callback=True),
                                                           self.db)
                final_handler = CallbackQueryHandler(handler_callable, pattern=handler.pattern)
                self.updater.dispatcher.add_handler(final_handler)
            else:
                assert False

    def _add_default_handlers(self):
        self.updater.dispatcher.add_handler(
            MessageHandler(TgFilters.all,
                           create_handler_callable(update_memberships, [], self.db)))
        self.updater.dispatcher.add_handler(
            MessageHandler(TgFilters.all,
                           create_handler_callable(self.pending_requests_dispatcher.dispatch, [], self.db)))

    @staticmethod
    def _normalize_filters(filters: list, for_callback: bool = False) -> list:
        if filters is None:
            filters = []
        if for_callback:
            filters += [FilterType.CALLBACK]
        return list(set(filters))
