# File with configuration parser (configuration.ini file).
# Since your bot may require having more settings stored in the file, feel free to add them to the __init__ and create()
# functions, as well as more normalization helpers.
import argparse
import configparser
import logging
import pathlib

from app.api.info import PROJECT_FULL_NAME, DEFAULT_CONFIG_PATH, DEFAULT_DB_PATH


class Config:
    def __init__(self, bot_token: str, admin_user: str, storage_dir: str):
        self.bot_token = bot_token
        self.admin_username = admin_user
        self.storage_dir = storage_dir

    @classmethod
    def create(cls) -> 'Config':
        config_path = cls._read_config_path_from_args()
        return cls._parse_config_file(config_path)

    # Private methods
    @staticmethod
    def _read_config_path_from_args() -> str:
        arg_parser = argparse.ArgumentParser(PROJECT_FULL_NAME)
        arg_parser.add_argument('--config', dest='config_path', type=str, default=str(DEFAULT_CONFIG_PATH),
                                help='Path to the configuration .ini file')
        args = arg_parser.parse_args()
        logging.info('Configuration file set to {}'.format(args.config_path))
        return args.config_path

    @classmethod
    def _parse_config_file(cls, config_path: str):
        config_path = pathlib.Path(config_path).resolve()
        assert config_path.is_file()
        ini_parser = configparser.ConfigParser()
        ini_parser.read(str(config_path))
        default_section = ini_parser['DEFAULT']
        return cls(default_section.get('telegram_bot_token', ''),
                   default_section.get('bot_admin_username', ''),
                   cls._normalize_dir(default_section.get('storage_directory', str(DEFAULT_DB_PATH))))

    @staticmethod
    def _normalize_dir(dir_str: str) -> str:
        return str(pathlib.Path(dir_str).resolve())
