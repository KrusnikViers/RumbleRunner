# File with configuration parser (configuration.ini file).
# Since your bot may require having more settings stored in the file, feel free to add them to the __init__ and get()
# functions, as well as more normalization helpers.
import argparse
import configparser
import logging
import pathlib

from app.bot.info import PROJECT_FULL_NAME, DEFAULT_CONFIG_PATH, DEFAULT_DB_PATH


class Config:
    # Add your values here
    def __init__(self, bot_token: str, admin_user: str, storage_dir: str):
        self.bot_token = bot_token
        self.admin_username = admin_user
        self.storage_dir = storage_dir

    # Note, that this method will always _parse_ current configuration.
    @classmethod
    def get(cls):
        # Parse command line for config file path, if needed.
        arg_parser = argparse.ArgumentParser(PROJECT_FULL_NAME)
        arg_parser.add_argument('--config', dest='config_path', type=str, default=str(DEFAULT_CONFIG_PATH),
                                help='Path to the configuration .ini file')
        args = arg_parser.parse_args()
        logging.info('Configuration file set to {}'.format(args.config_path))

        # Parse config
        config_path = pathlib.Path(args.config_path).resolve()
        assert config_path.exists()
        ini_parser = configparser.ConfigParser()
        ini_parser.read(str(config_path))
        default_section = ini_parser['DEFAULT']

        # Create config instance
        # Add your values here
        return cls(default_section.get('telegram_bot_token', ''),
                   default_section.get('bot_admin_username', ''),
                   cls._check_and_normalize_dir(default_section.get('storage_directory', str(DEFAULT_DB_PATH))))

    @staticmethod
    def _check_and_normalize_dir(dir_str: str) -> str:
        dir_path = pathlib.Path(dir_str)
        assert dir_path.is_dir()
        return str(dir_path.resolve())
