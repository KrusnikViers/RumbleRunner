from typing import Optional

from telegram import User as TgUser, Chat as TgChat

from base.database import DBHelpers
from base.database import SessionScope
from base.models.telegram_group import TelegramGroup
from base.models.telegram_user import TelegramUser


class ModelHelpers:
    @staticmethod
    def get_user_by_tg_id(tg_id: int) -> Optional[TelegramUser]:
        return SessionScope.session().query(TelegramUser).filter(TelegramUser.tg_id == tg_id).one_or_none()

    @staticmethod
    def get_from_tg_user(tg_user: TgUser) -> Optional[TelegramUser]:
        if tg_user.is_bot:
            return None
        return DBHelpers.select_and_update_by_tg_id(TelegramUser, tg_id=tg_user.id,
                                                    first_name=tg_user.first_name,
                                                    last_name=tg_user.last_name,
                                                    username=tg_user.username)

    @staticmethod
    def get_from_tg_chat(tg_chat: TgChat) -> Optional[TelegramGroup]:
        if tg_chat is None or tg_chat.type not in [TgChat.GROUP, TgChat.SUPERGROUP]:
            return None
        return DBHelpers.select_and_update_by_tg_id(TelegramGroup, tg_chat.id, name=tg_chat.title)
