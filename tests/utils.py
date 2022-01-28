import logging
from contextlib import ExitStack
from typing import Optional
from unittest import TestCase
from unittest.mock import MagicMock

from app.api.info import ROOT_DIR
from base.database.connection import DatabaseConnection
from base.database.session_scope import SessionScope
from base.handler.default.reporting import ReportsSender
from base.handler.wrappers.bot_scope import BotScope
from base.models import TelegramUser

TEST_DATA_DIR = ROOT_DIR.joinpath('tests', 'test_data').resolve()
TEST_DATA_TMP_DIR = TEST_DATA_DIR.joinpath('tmp')


class MatcherAny:
    def __eq__(self, _):
        return True


class BaseTestCase(TestCase):
    def setUp(self):
        super(BaseTestCase, self).setUp()
        logging.disable(logging.INFO)
        logging.disable(logging.WARNING)
        logging.disable(logging.ERROR)


class InBotTestCase(BaseTestCase):
    def __init__(self, *args, **kwargs):
        super(InBotTestCase, self).__init__(*args, **kwargs)
        self.connection: Optional[DatabaseConnection] = None
        self.bot_mock: Optional[MagicMock] = None

    def setUp(self):
        super(InBotTestCase, self).setUp()
        ReportsSender.set_admin(None)
        with ExitStack() as stack:
            self.bot_mock = MagicMock()
            stack.enter_context(BotScope(self.bot_mock))
            self.connection = DatabaseConnection.create_for_tests()
            stack.enter_context(SessionScope(self.connection))
            self.addCleanup(stack.pop_all().close)

    @staticmethod
    def new_user() -> TelegramUser:
        new_user_index = len(SessionScope.session().query(TelegramUser).all()) + 1
        user = TelegramUser(tg_id=1000 + new_user_index, first_name="user_{}".format(new_user_index))
        SessionScope.session().add(user)
        SessionScope.commit()
        return user
