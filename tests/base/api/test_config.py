import pathlib
import sys

from app.api.config import Config
from tests.utils import BaseTestCase, TEST_DATA_DIR


class TestConfig(BaseTestCase):
    def test_parsing(self):
        old_argv = sys.argv
        sys.argv = ['script_path', '--config', str(TEST_DATA_DIR.joinpath('example_config.ini'))]
        parsed_config = Config.create()
        sys.argv = old_argv

        self.assertEqual(parsed_config.bot_token, 'aaaa:bbbb')
        self.assertEqual(parsed_config.admin_username, 'superman')
        self.assertEqual(parsed_config.storage_dir, str(pathlib.Path('surely/relative\path').resolve()))
