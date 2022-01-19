from datetime import datetime

from alembic import command
from alembic.config import Config as AlembicConfig
from sqlalchemy.engine import Engine

from app.bot.info import APP_DIR


class MigrationScope:
    _scoped_engine = None

    @classmethod
    def current_engine(cls):
        return cls._scoped_engine

    def __init__(self, engine):
        self._old_engine = MigrationScope._scoped_engine
        self._engine = engine

    def __enter__(self):
        MigrationScope._scoped_engine = self._engine

    def __exit__(self, exc_type, exc_val, exc_tb):
        MigrationScope._scoped_engine = self._old_engine


def alembic_config():
    config = AlembicConfig()
    config.set_section_option('alembic', 'script_location', str(APP_DIR.joinpath('internal', 'storage', 'migrations')))
    config.set_section_option('alembic', 'file_template', '%%(slug)s_%%(rev)s')
    config.set_section_option('alembic', 'version_locations', str(APP_DIR.joinpath('bot', 'migrations')))
    config.set_section_option('handlers', 'keys', 'console')
    config.set_section_option('formatters', 'keys', 'generic')
    return config


def run_migrations(engine: Engine):
    with MigrationScope(engine):
        command.upgrade(alembic_config(), 'head')


def make_migrations(engine):
    message = 'auto_' + datetime.now().strftime('%Y%m%d_%H%M%S')
    with MigrationScope(engine):
        command.revision(alembic_config(), message=message, autogenerate=True)


def rollback_all(engine):
    with MigrationScope(engine):
        command.downgrade(alembic_config(), 'base')
