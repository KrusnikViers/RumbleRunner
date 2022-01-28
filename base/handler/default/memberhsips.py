from typing import Optional

from sqlalchemy import and_
from telegram import User as TgUser, Message as TgMessage

from base.database import SessionScope
from base.handler.wrappers import Context
from base.models import TelegramUser, TelegramGroup, TelegramUserInGroup
from base.models.helpers import ModelHelpers


class Memberships:
    @staticmethod
    def update(context: Context):
        if not context.group or not context.raw_data or not context.raw_data.update.effective_message:
            return
        tg_message: TgMessage = context.raw_data.update.effective_message
        for tg_user in tg_message.new_chat_members:
            Memberships._add_tg_user(tg_user, context.group)
        if context.sender:
            Memberships._add_user(context.sender, context.group)
        SessionScope.commit()
        if tg_message.left_chat_member is not None:
            Memberships._remove_user(tg_message.left_chat_member, context.group)
        SessionScope.commit()

    # Private methods
    @staticmethod
    def _add_tg_user(tg_user: TgUser, group: TelegramGroup):
        user = ModelHelpers.get_from_tg_user(tg_user)
        if user:
            Memberships._add_user(user, group)

    @staticmethod
    def _add_user(user: TelegramUser, group: TelegramGroup):
        if Memberships._get_membership(user, group) is None:
            new_membership = TelegramUserInGroup(telegram_user_id=user.id, telegram_group_id=group.id)
            SessionScope.session().add(new_membership)

    @staticmethod
    def _remove_user(tg_user: TgUser, group: TelegramGroup):
        user = ModelHelpers.get_from_tg_user(tg_user)
        if user:
            membership = Memberships._get_membership(user, group)
            if membership:
                SessionScope.session().delete(membership)

    @staticmethod
    def _get_membership(user: TelegramUser, group: TelegramGroup) -> Optional[TelegramUserInGroup]:
        return SessionScope.session().query(TelegramUserInGroup).filter(and_(
            TelegramUserInGroup.telegram_user_id == user.id,
            TelegramUserInGroup.telegram_group_id == group.id
        )).one_or_none()
