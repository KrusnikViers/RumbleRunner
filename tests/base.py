import logging
from unittest import TestCase

from sqlalchemy import MetaData

from app.internal.storage.connection import DatabaseConnection
from app.internal.storage.scoped_session import ScopedSession


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
        self.connection = DatabaseConnection(None, for_tests=True)

    def setUp(self):
        super(InBotTestCase, self).setUp()
        with ScopedSession(self.connection) as session:
            meta = MetaData(bind=self.connection, reflect=True)
            for table in reversed(meta.sorted_tables):
                session.execute(table.delete())
