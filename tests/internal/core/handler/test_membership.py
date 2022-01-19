from unittest.mock import MagicMock

from telegram import User as TgUser, Chat as TgChat, Message, Update

from app.internal.core.handler.context import Context
from app.internal.core.handler.memberhsip import update_memberships
from app.internal.storage.models.all import TelegramUser, TelegramGroup, TelegramUserInGroup
from app.internal.storage.scoped_session import ScopedSession
from tests.base import InBotTestCase


class TestMembershipUpdates(InBotTestCase):
    def test_no_crush_on_empty(self):
        update = MagicMock()
        context = Context(update, MagicMock(), self.connection)
        update_memberships(context)

    def test_add_remove_users(self):
        with ScopedSession(self.connection) as session:
            session.add(TelegramGroup(id=11, tg_id=1100))

            session.add(TelegramUser(id=1, tg_id=100, first_name='a'))
            session.add(TelegramUserInGroup(telegram_user_id=1, telegram_group_id=11))

            session.add(TelegramUser(id=2, tg_id=200, first_name='b'))
            session.add(TelegramUserInGroup(telegram_user_id=2, telegram_group_id=11))

            session.add(TelegramUser(id=3, tg_id=300, first_name='c'))

        update = Update(999, Message(888, None,
                                     TgChat(1100, TgChat.GROUP),
                                     from_user=TgUser(id=500, first_name='e', is_bot=False),
                                     new_chat_members=[TgUser(id=400, first_name='d', is_bot=False)],
                                     left_chat_member=TgUser(id=200, first_name='new_b', is_bot=False)))
        with Context(update, MagicMock(), self.connection) as context:
            update_memberships(context)

        with ScopedSession(self.connection) as session:
            group: TelegramGroup = session.query(TelegramGroup).first()
            self.assertListEqual([1, 4, 5], sorted([member.telegram_user.id for member in group.members]))
