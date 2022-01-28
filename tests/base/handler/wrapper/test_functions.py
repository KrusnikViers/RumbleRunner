from unittest.mock import MagicMock, PropertyMock

from telegram import Chat, User as TgUser, Message as TgMessage, Update, CallbackQuery

from app.api.command_list import PendingRequestId
from base.database.session_scope import SessionScope
from base.handler.wrappers.context import Context
from base.handler.wrappers.functions import WrapperFunctions
from base.handler.wrappers.requests import Requests
from base.models.all import TelegramUser, TelegramUserRequest
from base.routing.registration import ChatType
from tests.utils import InBotTestCase


class TestWrapperFunctions(InBotTestCase):
    def test_command_called(self):
        update = Update(000, message=TgMessage(111, None, Chat(222, Chat.PRIVATE), from_user=TgUser(333, 'a', False)))
        callable_fn = MagicMock()
        WrapperFunctions.command(callable_fn, ChatType.ALL, self.connection, update, MagicMock())
        callable_fn.assert_called_once()

    def test_callback_called(self):
        tg_user = TgUser(333, 'a', False)
        update = Update(000, callback_query=CallbackQuery(
            'id', from_user=tg_user, chat_instance='chat_instance', data='1::',
            message=TgMessage(666, MagicMock(), chat=Chat(888, Chat.PRIVATE), from_user=tg_user)))
        callable_fn = MagicMock()
        WrapperFunctions.callback(callable_fn, ChatType.ALL, self.connection, update, MagicMock())
        callable_fn.assert_called_once()

    def test_callback_called_personal(self):
        tg_user = TgUser(333, 'a', False)
        update = Update(000, callback_query=CallbackQuery(
            'id', from_user=tg_user, chat_instance='chat_instance', data='1:333:',
            message=TgMessage(666, MagicMock(), chat=Chat(888, Chat.PRIVATE), from_user=tg_user)))
        callable_fn = MagicMock()
        WrapperFunctions.callback(callable_fn, ChatType.ALL, self.connection, update, MagicMock())
        callable_fn.assert_called_once()

    def test_callback_wrong_user(self):
        tg_user = TgUser(333, 'a', False)
        update = Update(000, callback_query=CallbackQuery(
            'id', from_user=tg_user, chat_instance='chat_instance', data='1:444:',
            message=TgMessage(666, MagicMock(), chat=Chat(888, Chat.PRIVATE), from_user=tg_user)))
        callable_fn = MagicMock()
        WrapperFunctions.callback(callable_fn, ChatType.ALL, self.connection, update, MagicMock())
        callable_fn.assert_not_called()

    def test_command_wrong_chat_type(self):
        update = Update(000, message=TgMessage(111, None, Chat(222, Chat.PRIVATE), from_user=TgUser(333, 'a', False)))
        callable_fn = MagicMock()
        WrapperFunctions.command(callable_fn, ChatType.GROUP, self.connection, update, MagicMock())
        callable_fn.assert_not_called()


class TestRequestsDispatching(InBotTestCase):
    def test_no_sender(self):
        WrapperFunctions.request({}, self.connection, MagicMock(), MagicMock())

    def test_no_request(self):
        SessionScope.session().add(TelegramUser(tg_id=1, first_name='a'))
        SessionScope.commit()
        update = Update(000, message=TgMessage(111, None, Chat(222, Chat.PRIVATE), from_user=TgUser(1, 'a', False),
                                               text='test_message'))
        WrapperFunctions.request({}, self.connection, update, MagicMock())

    def test_no_handler(self):
        SessionScope.session().add(TelegramUser(tg_id=1, first_name='a'))
        SessionScope.commit()
        update = Update(000, message=TgMessage(111, None, Chat(222, Chat.PRIVATE), from_user=TgUser(1, 'a', False),
                                               text='test_message'))
        with Context.from_update(update, MagicMock()) as context:
            self.assertTrue(Requests.create(context, PendingRequestId.PREDEFINED_FOR_TESTS_1))
        WrapperFunctions.request({}, self.connection, update, MagicMock())

    def test_obsolete_type(self):
        SessionScope.session().add(TelegramUser(tg_id=1, first_name='a'))
        SessionScope.session().add(TelegramUserRequest(type='invalid', original_message_id=123, telegram_user_id=1))
        SessionScope.commit()
        update = Update(000, message=TgMessage(111, None, Chat(222, Chat.PRIVATE), from_user=TgUser(1, 'a', False),
                                               text='test_message'))
        WrapperFunctions.request({}, self.connection, update, MagicMock())

    def test_handler_exception(self):
        callable_fn = MagicMock()
        callable_fn.side_effect = TypeError()
        SessionScope.session().add(TelegramUser(tg_id=1, first_name='a'))
        SessionScope.commit()
        update = Update(000, message=TgMessage(111, None, Chat(222, Chat.PRIVATE), from_user=TgUser(1, 'a', False),
                                               text='test_message'))
        with Context.from_update(update, MagicMock()) as context:
            self.assertTrue(Requests.create(context, PendingRequestId.PREDEFINED_FOR_TESTS_1))
        WrapperFunctions.request({PendingRequestId.PREDEFINED_FOR_TESTS_1: callable_fn},
                                 self.connection, update, MagicMock())
        callable_fn.assert_called_once()

    def test_ok(self):
        callable_fn = MagicMock()
        SessionScope.session().add(TelegramUser(tg_id=1, first_name='a'))
        SessionScope.commit()
        update = Update(000, message=TgMessage(111, None, Chat(222, Chat.PRIVATE), from_user=TgUser(1, 'a', False),
                                               text='test_message'))
        with Context.from_update(update, MagicMock()) as context:
            self.assertTrue(Requests.create(context, PendingRequestId.PREDEFINED_FOR_TESTS_1))
        WrapperFunctions.request({PendingRequestId.PREDEFINED_FOR_TESTS_1: callable_fn},
                                 self.connection, update, MagicMock())
        callable_fn.assert_called_once()
