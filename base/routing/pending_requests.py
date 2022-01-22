import logging
from typing import Optional, Dict, Callable

from sqlalchemy import and_
from sqlalchemy.orm import Session

from base.handler.context.context import Context
from base.models.all import TelegramUserRequest, TelegramGroup, TelegramUser


class PendingRequests:
    @staticmethod
    def get(session: Session, user: TelegramUser, group: Optional[TelegramGroup]) -> Optional[TelegramUserRequest]:
        group_id = None if group is None else group.id
        return session.query(TelegramUserRequest).filter(
            and_(
                TelegramUserRequest.telegram_user_id == user.id,
                TelegramUserRequest.telegram_group_id == group_id)).one_or_none()

    @staticmethod
    def create(session: Session, pending_action: str, user: TelegramUser,
               group: Optional[TelegramGroup] = None) -> bool:
        if PendingRequests.get(session, user, group) is not None:
            return False
        session.add(TelegramUserRequest(type=pending_action,
                                        telegram_user_id=user.id,
                                        telegram_group_id=None if group is None else group.id))
        session.commit()
        return True

    @staticmethod
    def replace(session: Session, pending_action: str, user: TelegramUser,
                group: Optional[TelegramGroup] = None):
        existing_request = PendingRequests.get(session, user, group)
        if existing_request is not None:
            session.delete(existing_request)
        session.add(TelegramUserRequest(type=pending_action,
                                        telegram_user_id=user.id,
                                        telegram_group_id=None if group is None else group.id))
        session.commit()


class PendingRequestsDispatcher:
    def __init__(self, handlers: Dict[str, Callable[[Context], Optional[str]]]):
        self.handlers = handlers

    def dispatch(self, context: Context):
        if not context.sender or not context.data.text:
            return

        pending_request = PendingRequests.get(context.session, context.sender, context.group)
        if pending_request is None:
            return

        request_type = pending_request.type
        if request_type not in self.handlers:
            logging.warning('Bad handler request type: {}'.format(request_type))
            return

        context.pending_request = pending_request
        self.handlers[pending_request.type](context)
