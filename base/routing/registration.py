from enum import Enum, unique
from typing import Callable, Optional

from app.api.command_list import CallbackId, PendingRequestId
from base.handler.wrappers.context import Context


@unique
class ChatType(Enum):
    ALL = 0
    PRIVATE = 1
    GROUP = 2


class CommandHandlerReg:
    def __init__(self, commands: list, callable_fn: Callable[[Context], Optional[str]],
                 chat_type: ChatType = ChatType.ALL):
        self.commands = commands
        self.callable_fn = callable_fn
        self.chat_type = chat_type


class CallbackHandlerReg:
    def __init__(self, callback_id: CallbackId, callable_fn: Callable[[Context], Optional[str]],
                 chat_type: ChatType = ChatType.ALL):
        self.pattern = '^{0}:.*:.*$'.format(int(callback_id))
        self.callable_fn = callable_fn
        self.chat_type = chat_type


class PendingRequestHandlerReg:
    def __init__(self, request_type: PendingRequestId, callable_fn: Callable[[Context], Optional[str]]):
        self.request_type = request_type
        self.callable_fn = callable_fn
