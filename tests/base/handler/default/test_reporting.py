from unittest.mock import MagicMock

from app.config import Config
from base.database.scoped_session import ScopedSession
from base.handler.context.context import Context
from base.handler.default.reporting import ReportsSender
from base.models.all import TelegramUser
from tests.utils import InBotTestCase, MatcherAny


class TestReports(InBotTestCase):
    def test_no_sender_no_crash(self):
        ReportsSender.instance = None
        ReportsSender.forward_user_message(MagicMock())
        ReportsSender.report_exception(None, self.connection)

    def test_send_report(self):
        config = Config('', 'admin', '')
        bot = MagicMock()
        with ScopedSession(self.connection) as session:
            session.add(TelegramUser(tg_id=111, first_name='Other', username='other'))
            session.add(TelegramUser(tg_id=123, first_name='Admin', username='admin'))

        ReportsSender.instance = ReportsSender(bot, config)
        with ScopedSession(self.connection) as session:
            ReportsSender.forward_user_message(Context(MagicMock(), MagicMock(), self.connection))
            bot.forward_message.assert_called_once_with(123, MatcherAny(), MatcherAny())

            ReportsSender.report_exception(MagicMock(), session)
            bot.send_message.assert_called_once_with(123, MatcherAny())
