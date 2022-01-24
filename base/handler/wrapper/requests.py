from typing import Optional

from sqlalchemy import and_

from app.api.command_list import PendingRequestId
from base.handler.wrapper.context import Context
from base.models.all import TelegramUserRequest


class Requests:
    @staticmethod
    def get(context: Context) -> Optional[TelegramUserRequest]:
        return context.session.query(TelegramUserRequest).filter(
            and_(
                TelegramUserRequest.telegram_user_id == context.sender.id,
                TelegramUserRequest.telegram_group_id == context.group_id)).one_or_none()

    @staticmethod
    def create(context: Context, request_type: PendingRequestId, additional_data: Optional[str] = None) -> bool:
        if Requests.get(context) is not None:
            return False
        context.session.add(TelegramUserRequest(type=request_type.value,
                                                telegram_user_id=context.sender.id,
                                                telegram_group_id=context.group_id,
                                                original_message_id=context.actions.msg_id,
                                                additional_data=additional_data))
        context.session.commit()
        return True

    @staticmethod
    def replace(context: Context, request_type: PendingRequestId, additional_data: Optional[str] = None):
        existing_request = Requests.get(context)
        if existing_request is not None:
            context.session.delete(existing_request)
            context.session.commit()
        context.session.add(TelegramUserRequest(type=request_type.value,
                                                telegram_user_id=context.sender.id,
                                                telegram_group_id=context.group_id,
                                                original_message_id=context.actions.msg_id,
                                                additional_data=additional_data))
        context.session.commit()
