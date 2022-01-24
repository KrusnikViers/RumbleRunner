from base.database.connection import DatabaseConnection
from tests.utils import BaseTestCase, TEST_DATA_TMP_DIR


class TestConnection(BaseTestCase):
    def test_create_new_db_connection(self):
        connection = DatabaseConnection.create(str(TEST_DATA_TMP_DIR))
        self.assertEqual(connection.engine.name, 'sqlite')
        self.assertTrue(str(connection.engine.url).endswith('tmp/storage.db'))
        TEST_DATA_TMP_DIR.joinpath('storage.db').unlink()
