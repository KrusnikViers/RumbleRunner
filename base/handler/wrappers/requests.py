from typing import Optional

from sqlalchemy import and_

from app import PendingRequestId
from base.database import SessionScope
from base.database.helpers import DBHelpers
from base.handler.wrappers.context import Context
from base.models import TelegramUserRequest, TelegramUser, TelegramGroup


class Requests:
    @staticmethod
    def get_from_raw_data(user_tg_id: int, group_tg_id: int) -> Optional[TelegramUserRequest]:
        if not (user := DBHelpers.select_by_tg_id(TelegramUser, user_tg_id)):
            return None
        group = DBHelpers.select_by_tg_id(TelegramGroup, group_tg_id)
        group_id = group.id if group else None
        return SessionScope.session().query(TelegramUserRequest).filter(and_(
            TelegramUserRequest.telegram_user_id == user.id,
            TelegramUserRequest.telegram_group_id == group_id)).one_or_none()

    @staticmethod
    def create(context: Context, request_type: PendingRequestId, original_message_id=None,
               additional_data: Optional[str] = None) -> bool:
        if context.request is not None:
            return False
        context.request = TelegramUserRequest(type=request_type.value,
                                              telegram_user_id=context.sender.id,
                                              telegram_group_id=Requests._group_id(context),
                                              original_message_id=original_message_id,
                                              additional_data=additional_data)
        SessionScope.session().add(context.request)
        SessionScope.commit()
        return True

    @staticmethod
    def replace(context: Context, request_type: PendingRequestId, original_message_id=None,
                additional_data: Optional[str] = None):
        if context.request is not None:
            SessionScope.session().delete(context.request)
        context.request = TelegramUserRequest(type=request_type.value,
                                              telegram_user_id=context.sender.id,
                                              telegram_group_id=Requests._group_id(context),
                                              original_message_id=original_message_id,
                                              additional_data=additional_data)
        SessionScope.session().add(context.request)
        SessionScope.commit()

    @staticmethod
    def delete(context: Context) -> bool:
        if context.request is None:
            return False
        SessionScope.session().delete(context.request)
        SessionScope.commit()
        context.request = None
        return True

    @staticmethod
    def _group_id(context: Context):
        return None if context.group is None else context.group.id
