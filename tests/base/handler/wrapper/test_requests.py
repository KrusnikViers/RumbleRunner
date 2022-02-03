from app import PendingRequestId
from base import Context, Message, Requests
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

    def test_request_for_missing_user(self):
        another_user = self.new_user()
        non_existing_user_id = 999
        self.assertNotEqual(another_user.tg_id, non_existing_user_id)
        self.assertIsNone(Requests.get_from_raw_data(non_existing_user_id, 111))
