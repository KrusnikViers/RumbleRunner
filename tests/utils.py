import logging
from unittest import TestCase

from app.api.info import ROOT_DIR
from base.database.connection import DatabaseConnection
from base.handler.default.reporting import ReportsSender


class MatcherAny:
    def __eq__(self, _):
        return True


TEST_DATA_DIR = ROOT_DIR.joinpath('tests', 'test_data').resolve()
TEST_DATA_TMP_DIR = TEST_DATA_DIR.joinpath('tmp')


class BaseTestCase(TestCase):
    def setUp(self):
        super(BaseTestCase, self).setUp()
        logging.disable(logging.INFO)
        logging.disable(logging.WARNING)
        logging.disable(logging.ERROR)


class InBotTestCase(BaseTestCase):
    def __init__(self, *args, **kwargs):
        super(InBotTestCase, self).__init__(*args, **kwargs)

    def setUp(self):
        super(InBotTestCase, self).setUp()
        ReportsSender.instance = None
        self.connection = DatabaseConnection.create_for_tests()
