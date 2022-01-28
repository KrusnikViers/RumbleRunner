import functools
from typing import List, Union

from telegram.ext import CallbackQueryHandler, CommandHandler, MessageHandler, \
    Updater, Filters as TgFilters

from base.database import DatabaseConnection
from base.handler import Memberships
from base.handler.wrappers.functions import WrapperFunctions
from base.routing.registration import CallbackHandlerReg, CommandHandlerReg, PendingRequestHandlerReg


class Dispatcher:
    def __init__(self, updater: Updater, db_connection: DatabaseConnection,
                 message_handlers: List[Union[CommandHandlerReg, CallbackHandlerReg, PendingRequestHandlerReg]]):
        self.db = db_connection
        self.updater = updater

        self._add_custom_handlers(message_handlers)
        self._add_default_handlers()

    def _add_custom_handlers(self, message_handlers: list):
        pending_actions_dict = dict()
        for handler in message_handlers:
            if isinstance(handler, CommandHandlerReg):
                resulting_callable = functools.partial(
                    WrapperFunctions.command, handler.callable_fn, handler.chat_type, self.db)
                self.updater.dispatcher.add_handler(CommandHandler(handler.commands, resulting_callable))
            elif isinstance(handler, CallbackHandlerReg):
                resulting_callable = functools.partial(
                    WrapperFunctions.callback, handler.callable_fn, handler.chat_type, self.db)
                self.updater.dispatcher.add_handler(CallbackQueryHandler(resulting_callable, pattern=handler.pattern))
            elif isinstance(handler, PendingRequestHandlerReg):
                pending_actions_dict[handler.request_type] = handler.callable_fn
            else:
                raise ValueError
        if pending_actions_dict:
            resulting_callable = functools.partial(WrapperFunctions.request, pending_actions_dict, self.db)
            self.updater.dispatcher.add_handler(MessageHandler(TgFilters.text, resulting_callable))

    def _add_default_handlers(self):
        memberships_update_callable = functools.partial(
            WrapperFunctions.universal, Memberships.update, self.db)
        self.updater.dispatcher.add_handler(MessageHandler(TgFilters.all, memberships_update_callable))
