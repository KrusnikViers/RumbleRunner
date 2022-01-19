from unittest.mock import MagicMock

from app.internal.core.handler.reporting import ReportsSender
from tests.base import InBotTestCase


class TestReports(InBotTestCase):
    def test_no_sender_no_crash(self):
        ReportsSender.instance = None
        ReportsSender.forward_user_message(MagicMock())
        ReportsSender.report_exception(None, self.connection)
