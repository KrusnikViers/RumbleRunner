from unittest.mock import MagicMock

from app.bot.config import Config
from app.internal.core.handler.reporting import ReportsSender
from app.internal.storage.models.all import TelegramUser
from app.internal.storage.scoped_session import ScopedSession
from tests.base import InBotTestCase, MatcherAny
from app.internal.core.handler.context import Context


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
        ReportsSender.forward_user_message(Context(MagicMock(), MagicMock(), self.connection))
        bot.forward_message.assert_called_once_with(123, MatcherAny(), MatcherAny())

        ReportsSender.report_exception(MagicMock(), self.connection)
        bot.send_message.assert_called_once_with(123, MatcherAny())
