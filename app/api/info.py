# File with common definitions, that are constant literals or could be resolved on the bot start.
import os
import pathlib

APP_DIR: pathlib.Path = pathlib.Path(os.path.realpath(__file__)).parent.parent.resolve()
ROOT_DIR: pathlib.Path = APP_DIR.parent.resolve()

DEFAULT_DB_PATH: pathlib.Path = ROOT_DIR.joinpath('/build').resolve()
DEFAULT_CONFIG_PATH: pathlib.Path = ROOT_DIR.joinpath('configuration.ini').resolve()

PROJECT_NAME: str = 'RumbleRunner'
PROJECT_VERSION: str = '1.0.1'
PROJECT_FULL_NAME: str = '{} v{}'.format(PROJECT_NAME, PROJECT_VERSION)

# Add custom definitions below.
