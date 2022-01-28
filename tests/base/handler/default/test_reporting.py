from unittest.mock import MagicMock

from base.database.session_scope import SessionScope
from base.handler.default.reporting import ReportsSender
from base.handler.wrappers.context import Context
from base.models.all import TelegramUser
from tests.utils import InBotTestCase, MatcherAny


class TestReports(InBotTestCase):
    def test_no_receiver_no_crash(self):
        ReportsSender.set_admin(None)
        ReportsSender.report_exception(None)

    def test_send_report(self):
        SessionScope.session().add(TelegramUser(tg_id=111, first_name='Other', username='other'))
        SessionScope.session().add(TelegramUser(tg_id=123, first_name='Admin', username='admin'))

        ReportsSender.set_admin('admin')
        ReportsSender.report_exception(MagicMock())
        self.bot_mock.send_message.assert_called_once_with(123, MatcherAny())
