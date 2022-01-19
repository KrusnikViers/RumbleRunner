from typing import Optional

from sqlalchemy import and_

from app.internal.core.handler.context import Context
from app.internal.storage.models.all import TelegramUser, TelegramUserInGroup
from app.internal.storage.util import select_and_update_by_tg_id


def _get_membership(context: Context, user_tg_id: int) -> Optional[TelegramUserInGroup]:
    return context.session.query(TelegramUserInGroup).where(and_(
        TelegramUserInGroup.telegram_group.tg_id == context.update.effective_chat.id,
        TelegramUserInGroup.telegram_user.tg_id == user_tg_id
    )).first()


def update_memberships(context: Context):
    if not context.group:
        return
    users_to_create = [tg_user for tg_user in context.update.message.new_chat_members if not tg_user.is_bot]
    user_to_remove = context.update.message.left_chat_member
    if user_to_remove is None or user_to_remove.id != context.sender.tg_id:
        sender_membership = _get_membership(context, context.update.effective_user.id)
        if not sender_membership:
            users_to_create += [context.update.effective_user]

    for user_to_create in users_to_create:
        if not _get_membership(context, user_to_create.id):
            user_model = select_and_update_by_tg_id(context.session, TelegramUser, user_to_create.id,
                                                    first_name=user_to_create.first_name,
                                                    last_name=user_to_create.last_name,
                                                    username=user_to_create.username)
            new_membership = TelegramUserInGroup(telegram_user=user_model, telegram_group=context.group)
            context.session.add(new_membership)

    if user_to_remove is not None:
        expired_membership = _get_membership(context, user_to_remove.id)
        if expired_membership:
            context.session.delete(expired_membership)
