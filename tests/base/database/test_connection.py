from app.api.config import Config
from base.database.connection import DatabaseConnection
from tests.utils import BaseTestCase


class TestConnection(BaseTestCase):
    def test_db_url(self):
        config = Config('', '', '/some/test/path')
        self.assertEqual(DatabaseConnection.create_database_url(config, for_tests=True), "sqlite://")
        self.assertEqual(DatabaseConnection.create_database_url(config, for_tests=False),
                         "sqlite:////some/test/path/storage.db")
