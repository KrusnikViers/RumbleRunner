import logging
from typing import Optional

from sqlalchemy import and_

from app.internal.core.handler.context import Context
from app.internal.storage.models.all import TelegramUserRequest


def get_pending_request(context: Context) -> Optional[TelegramUserRequest]:
    return context.session.query(TelegramUserRequest).where(
        and_(
            TelegramUserRequest.telegram_user == context.sender,
            TelegramUserRequest.telegram_group == context.group)).first()


# Returns false, if user already has pending request in this chat/group
def try_create_pending_request(context: Context, request_type: str) -> bool:
    if get_pending_request(context) is not None:
        return False
    context.session.add(
        TelegramUserRequest(type=request_type, telegram_user=context.sender, telegram_group=context.group))
    return True


class PendingRequestsDispatcher:
    def __init__(self, handlers: dict):
        self.handlers = handlers

    def maybe_dispatch(self, context: Context):
        if not context.sender or not context.update.message:
            return

        pending_request = get_pending_request(context)
        if pending_request is None:
            return

        request_type = pending_request.type
        if request_type not in self.handlers:
            logging.warning('Bad handler request type: {}'.format(request_type))
            return

        context.pending_request = pending_request
        self.handlers[request_type](context)
