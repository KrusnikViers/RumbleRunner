from app import PendingRequestId
from base import SessionScope, Context, Message, Requests, TelegramUserRequest
from base.handler.default.canceling import delete_message, delete_message_and_pending_request
from tests.utils import InBotTestCase


class TestCancelingHandlers(InBotTestCase):
    def test_delete_message(self):
        delete_message(Context(message=Message(chat_id=111, message_id=222)))
        self.bot_mock.delete_message.assert_called_once_with(chat_id=111, message_id=222)

    def test_delete_pending_message(self):
        with Context(sender=self.new_user(), message=Message(chat_id=111, message_id=222)) as context:
            context.sender = self.new_user()
            self.assertTrue(Requests.create(context, PendingRequestId.PREDEFINED_FOR_TESTS_1))
            self.assertIsNotNone(context.request)

            with self.bot_mock():
                delete_message_and_pending_request(context)
                self.bot_mock.delete_message.assert_called_once_with(chat_id=111, message_id=222)
            self.assertIsNone(context.request)
            self.assertIsNone(SessionScope.session().query(TelegramUserRequest).first())
