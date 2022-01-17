import sys

from app.bot.config import Config
from app.bot.info import ROOT_DIR
from tests.base import BaseTestCase


class TestConfig(BaseTestCase):
    def test_parsing(self):
        old_argv = sys.argv
        sys.argv = ['script_path', '--config', str(ROOT_DIR.joinpath('tests', 'test_data', 'example_config.ini'))]
        parsed_config = Config.get()
        sys.argv = old_argv

        self.assertEqual(parsed_config.bot_token, 'aaaa:bbbb')
        self.assertEqual(parsed_config.admin_username, 'superman')
        self.assertEqual(parsed_config.storage_dir, 'C:\\in\\a\\distant\\land')
