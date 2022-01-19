import logging
from typing import Optional

from sqlalchemy import and_

from app.internal.core.handler.context import Context
from app.internal.core.handler.reporting import ReportsSender
from app.internal.storage.models.all import TelegramUserRequest


def _get_group_id(context: Context) -> Optional[int]:
    return context.group.id if context.group else None


def get_pending_request(context: Context) -> Optional[TelegramUserRequest]:
    return context.session.query(TelegramUserRequest).filter(
        and_(
            TelegramUserRequest.telegram_user_id == context.sender.id,
            TelegramUserRequest.telegram_group_id == _get_group_id(context))).first()


# Returns false, if user already has pending request in this chat/group
def try_create_pending_request(context: Context, request_type: str) -> bool:
    if get_pending_request(context) is not None:
        return False
    context.session.add(
        TelegramUserRequest(type=request_type,
                            telegram_user_id=context.sender.id,
                            telegram_group_id=_get_group_id(context)))
    return True


class PendingRequestsDispatcher:
    def __init__(self, handlers: dict):
        self.handlers = handlers

    def dispatch(self, context: Context):
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
        try:
            self.handlers[request_type](context)
        except Exception:
            ReportsSender.report_exception(context.update, context.session)
