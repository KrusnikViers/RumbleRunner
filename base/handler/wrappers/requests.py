from typing import Optional

from app import PendingRequestId
from base.database import SessionScope
from base.handler.wrappers.context import Context
from base.models import TelegramUserRequest


class Requests:
    @staticmethod
    def create(context: Context, request_type: PendingRequestId, additional_data: Optional[str] = None) -> bool:
        if context.request is not None:
            return False
        context.request = TelegramUserRequest(type=request_type.value,
                                              telegram_user_id=context.sender.id,
                                              telegram_group_id=Requests._group_id(context),
                                              original_message_id=context.message.message_id,
                                              additional_data=additional_data)
        SessionScope.session().add(context.request)
        SessionScope.commit()
        return True

    @staticmethod
    def replace(context: Context, request_type: PendingRequestId, additional_data: Optional[str] = None):
        if context.request is not None:
            SessionScope.session().delete(context.request)
        context.request = TelegramUserRequest(type=request_type.value,
                                              telegram_user_id=context.sender.id,
                                              telegram_group_id=Requests._group_id(context),
                                              original_message_id=context.message.message_id,
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
