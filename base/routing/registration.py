from typing import Callable, Optional

from app.routing.callbacks import CallbackIds
from app.routing.pending_requests import PendingRequestType
from base.handler.context.context import Context
from base.handler.context.definitions import ChatType


class CommandHandlerReg:
    def __init__(self, commands: list, callable_fn: Callable[[Context], Optional[str]],
                 chat_type: ChatType = ChatType.ALL):
        self.commands = commands
        self.callable_fn = callable_fn
        self.chat_type = chat_type


class CallbackHandlerReg:
    def __init__(self, callback_id: CallbackIds, callable_fn: Callable[[Context], Optional[str]],
                 chat_type: ChatType = ChatType.ALL):
        self.pattern = '^{0}:.*:.*$'.format(int(callback_id))
        self.callable_fn = callable_fn
        self.chat_type = chat_type


class PendingRequestHandlerReg:
    def __init__(self, request_type: PendingRequestType, callable_fn: Callable[[Context], Optional[str]]):
        self.request_type = request_type
        self.callable_fn = callable_fn
