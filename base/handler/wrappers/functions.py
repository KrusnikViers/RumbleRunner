import logging
from typing import Callable, Optional, Dict

from telegram import Update, Chat
from telegram.ext import CallbackContext

from app.api.command_list import value_to_enum, PendingRequestId
from base.database.connection import DatabaseConnection
from base.database.session_scope import SessionScope
from base.handler.default.memberhsips import Memberships
from base.handler.default.reporting import ReportsSender
from base.handler.helpers.actions import Actions
from base.handler.wrappers.context import Context
from base.handler.wrappers.message import CallbackData
from base.routing.registration import ChatType


class _Filter:
    @staticmethod
    def is_chat_type_correct(chat_type: ChatType, update: Update) -> bool:
        return chat_type == ChatType.ALL or \
               (chat_type == ChatType.PRIVATE and update.effective_chat.type == Chat.PRIVATE) or \
               (chat_type == ChatType.GROUP and update.effective_chat.type in [Chat.GROUP, Chat.SUPERGROUP])

    @staticmethod
    def sender_and_chat_are_valid(update: Update) -> bool:
        has_errors = (not update.effective_chat or not update.effective_user) or \
                     (update.effective_chat.type not in [Chat.GROUP, Chat.SUPERGROUP, Chat.PRIVATE]) or \
                     update.effective_user.is_bot
        return not has_errors

    @staticmethod
    def has_enough_data(update: Update, is_callback: bool):
        if is_callback:
            return update.callback_query is not None
        else:
            return update.message is not None


class WrapperFunctions:
    @staticmethod
    def _common_handler_body(handler_fn: Callable[[Context], Optional[str]], database_connection: DatabaseConnection,
                             update: Update, callback_context: CallbackContext):
        with SessionScope(database_connection):
            with Context.from_update(update, callback_context) as context:
                try:
                    Memberships.update(context)
                    answer = handler_fn(context)
                    if answer is not None:
                        Actions.send_message(answer, message=context.message)
                except Exception:
                    ReportsSender.report_exception(update)

    @staticmethod
    def command(handler_fn: Callable[[Context], Optional[str]], chat_type: ChatType,
                database_connection: DatabaseConnection,
                # Up to this point, arguments are predefined by the *Reg function.
                update: Update, callback_context: CallbackContext):
        is_update_correct = _Filter.is_chat_type_correct(chat_type, update) and \
                            _Filter.sender_and_chat_are_valid(update) and \
                            _Filter.has_enough_data(update, is_callback=False)
        if is_update_correct:
            WrapperFunctions._common_handler_body(handler_fn, database_connection, update, callback_context)

    @staticmethod
    def callback(handler_fn: Callable[[Context], Optional[str]], chat_type: ChatType,
                 database_connection: DatabaseConnection,
                 # Up to this point, arguments are predefined by the *Reg function.
                 update: Update, callback_context: CallbackContext):
        is_update_correct = _Filter.is_chat_type_correct(chat_type, update) and \
                            _Filter.sender_and_chat_are_valid(update) and \
                            _Filter.has_enough_data(update, is_callback=True)
        callback_data = CallbackData.parse(update.callback_query.data)
        if callback_data.user_id is not None:
            is_update_correct = is_update_correct and update.effective_user.id == callback_data.user_id
        if is_update_correct:
            WrapperFunctions._common_handler_body(handler_fn, database_connection, update, callback_context)

    @staticmethod
    def universal(handler_fn: Callable[[Context], Optional[str]], database_connection: DatabaseConnection,
                  # Up to this point, arguments are predefined by the *Reg function.
                  update: Update, callback_context: CallbackContext):
        WrapperFunctions._common_handler_body(handler_fn, database_connection, update, callback_context)

    # Special treatment case for pending requests
    @staticmethod
    def request(handlers_dict: Dict[str, Callable[[Context], Optional[str]]],
                database_connection: DatabaseConnection,
                # Up to this point, arguments are predefined by the *Reg function.
                update: Update, callback_context: CallbackContext):
        with SessionScope(database_connection):
            with Context.from_update(update, callback_context) as context:
                try:
                    Memberships.update(context)
                    if context.request is None:
                        return

                    request_type = value_to_enum(PendingRequestId, context.request.type)
                    if not request_type:
                        return
                    if request_type not in handlers_dict:
                        logging.warning('Missing handler for request type: {}'.format(context.request.type))
                        return

                    answer = handlers_dict[request_type](context)
                    if answer is not None:
                        Actionssend_message(answer, message=context.message)
                except Exception:
                    ReportsSender.report_exception(update)
