from app.api.command_list import PendingRequestId
from base.handler.wrappers.context import Context
from base.handler.wrappers.message import Message
from base.handler.wrappers.requests import Requests
from tests.utils import InBotTestCase


class TestRequests(InBotTestCase):
    def test_replace_request(self):
        with Context(message=Message(message_id=111), sender=self.new_user()) as context:
            self.assertTrue(Requests.create(context, PendingRequestId.PREDEFINED_FOR_TESTS_1))
            self.assertEqual(context.request.type, PendingRequestId.PREDEFINED_FOR_TESTS_1)

            Requests.replace(context, PendingRequestId.PREDEFINED_FOR_TESTS_2)
            self.assertEqual(context.request.type, PendingRequestId.PREDEFINED_FOR_TESTS_2)

    def test_duplicate_request(self):
        with Context(message=Message(message_id=111), sender=self.new_user()) as context:
            self.assertTrue(Requests.create(context, PendingRequestId.PREDEFINED_FOR_TESTS_1))
            self.assertFalse(Requests.create(context, PendingRequestId.PREDEFINED_FOR_TESTS_1))

    def test_request_missing(self):
        with Context(message=Message(message_id=111), sender=self.new_user()) as context:
            self.assertFalse(Requests.delete(context))
