import functools
from typing import Callable, Dict, Optional, List, Union

from telegram.ext import CallbackQueryHandler, CommandHandler, MessageHandler, \
    Updater, Filters as TgFilters

from base.database.connection import DatabaseConnection
from base.handler.context.context import Context
from base.handler.context.wrapper_functions import WrapperFunctions
from base.handler.default.memberhsips import Memberships
from base.routing.pending_requests import PendingRequestsDispatcher
from base.routing.registration import CallbackHandlerReg, CommandHandlerReg


class Dispatcher:
    def __init__(self, updater: Updater, db_connection: DatabaseConnection,
                 message_handlers: List[Union[CommandHandlerReg, CallbackHandlerReg]],
                 pending_requests_handlers: Dict[str, Callable[[Context], Optional[str]]]):
        self.db = db_connection
        self.updater = updater
        self.pending_requests_dispatcher = PendingRequestsDispatcher(pending_requests_handlers)

        self._add_custom_handlers(message_handlers)
        self._add_default_handlers()

    def _add_custom_handlers(self, message_handlers: list):
        for handler in message_handlers:
            if isinstance(handler, CommandHandlerReg):
                resulting_callable = functools.partial(
                    WrapperFunctions.command, handler.callable_fn, handler.chat_type, self.db)
                self.updater.dispatcher.add_handler(CommandHandler(handler.commands, resulting_callable))
            elif isinstance(handler, CallbackHandlerReg):
                resulting_callable = functools.partial(
                    WrapperFunctions.callback, handler.callable_fn, handler.chat_type, self.db)
                self.updater.dispatcher.add_handler(CallbackQueryHandler(resulting_callable, pattern=handler.pattern))
            else:
                raise ValueError

    def _add_default_handlers(self):
        pending_requests_callable = functools.partial(
            WrapperFunctions.universal, self.pending_requests_dispatcher.dispatch, self.db)
        self.updater.dispatcher.add_handler(MessageHandler(TgFilters.text, pending_requests_callable))

        memberships_update_callable = functools.partial(
            WrapperFunctions.universal, Memberships.update, self.db)
        self.updater.dispatcher.add_handler(MessageHandler(TgFilters.all, memberships_update_callable))
