from unittest.mock import MagicMock

from telegram import User as TgUser, Chat as TgChat, Message, Update

from base.database.session_scope import SessionScope
from base.handler.default.memberhsips import Memberships
from base.handler.wrappers.context import Context
from base.models.all import TelegramUser, TelegramGroup, TelegramUserInGroup
from tests.utils import InBotTestCase


class TestMembershipUpdates(InBotTestCase):
    def test_no_crush_on_empty(self):
        context = Context(self.connection)
        Memberships.update(context)

    def test_add_group_and_user_from_notification(self):
        update = Update(999, Message(888, MagicMock(),
                                     TgChat(1010, TgChat.GROUP, title='Test Group'),
                                     from_user=TgUser(400, 'name', is_bot=False)))
        with Context.from_update(update, MagicMock()) as context:
            Memberships.update(context)

        group: TelegramGroup = SessionScope.session().query(TelegramGroup).first()
        self.assertEqual(group.name, 'Test Group')
        self.assertEqual(group.tg_id, 1010)

        user: TelegramUser = SessionScope.session().query(TelegramUser).first()
        self.assertEqual(user.tg_id, 400)
        self.assertEqual(user.first_name, 'name')

        membership: TelegramUserInGroup = SessionScope.session().query(TelegramUserInGroup).first()
        self.assertEqual(membership.telegram_group_id, group.id)
        self.assertEqual(membership.telegram_user_id, user.id)

    def test_add_user_from_field(self):
        SessionScope.session().add(TelegramGroup(id=11, tg_id=1100, name='tgroup'))
        SessionScope.session().add(TelegramUser(id=1, tg_id=100, first_name='a'))
        SessionScope.session().add(TelegramUser(id=2, tg_id=200, first_name='b'))
        SessionScope.session().add(TelegramUserInGroup(telegram_user_id=1, telegram_group_id=11))

        update = Update(999, Message(888, MagicMock(),
                                     TgChat(1100, TgChat.GROUP, title='tgroup'),
                                     from_user=TgUser(id=100, first_name='a', is_bot=False),
                                     new_chat_members=[TgUser(id=200, first_name='b', is_bot=False)]))
        with Context.from_update(update, MagicMock()) as context:
            Memberships.update(context)

        group: TelegramGroup = SessionScope.session().query(TelegramGroup).first()
        self.assertListEqual([1, 2], sorted([member.telegram_user.id for member in group.members]))

    def test_remove_user_from_field(self):
        SessionScope.session().add(TelegramGroup(id=11, tg_id=1100, name='tgroup'))
        SessionScope.session().add(TelegramUser(id=1, tg_id=100, first_name='a'))
        SessionScope.session().add(TelegramUser(id=2, tg_id=200, first_name='b'))
        SessionScope.session().add(TelegramUserInGroup(telegram_user_id=1, telegram_group_id=11))
        SessionScope.session().add(TelegramUserInGroup(telegram_user_id=2, telegram_group_id=11))

        update = Update(999, Message(888, MagicMock(),
                                     TgChat(1100, TgChat.GROUP, title='tgroup'),
                                     from_user=TgUser(id=100, first_name='a', is_bot=False),
                                     left_chat_member=TgUser(id=200, first_name='b', is_bot=False)))
        with Context.from_update(update, MagicMock()) as context:
            Memberships.update(context)

        group: TelegramGroup = SessionScope.session().query(TelegramGroup).first()
        self.assertListEqual([1], sorted([member.telegram_user.id for member in group.members]))
