from datetime import datetime

from alembic import command
from alembic.config import Config as AlembicConfig
from sqlalchemy.engine import Engine

from app.info import ROOT_DIR


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


class MigrationEngine:
    @staticmethod
    def _alembic_config():
        config = AlembicConfig()
        config.set_section_option('alembic', 'script_location', str(ROOT_DIR.joinpath('base', 'database', 'alembic')))
        config.set_section_option('alembic', 'file_template', '%%(slug)s_%%(rev)s')
        config.set_section_option('alembic', 'version_locations', str(ROOT_DIR.joinpath('app', 'migrations')))
        config.set_section_option('handlers', 'keys', 'console')
        config.set_section_option('formatters', 'keys', 'generic')
        return config

    def __init__(self, engine: Engine):
        self.engine = engine

    def run_migrations(self):
        with MigrationScope(self.engine):
            command.upgrade(MigrationEngine._alembic_config(), 'head')

    def make_migrations(self):
        message = 'auto_' + datetime.now().strftime('%Y%m%d_%H%M%S')
        with MigrationScope(self.engine):
            command.revision(MigrationEngine._alembic_config(), message=message, autogenerate=True)

    def rollback_all(self):
        with MigrationScope(self.engine):
            command.downgrade(MigrationEngine._alembic_config(), 'base')
