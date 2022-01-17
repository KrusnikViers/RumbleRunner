import os
from datetime import datetime

import alembic.config

from app.bot.info import APP_DIR


class MigrationScope:
    _scoped_engine = None

    @classmethod
    def current_engine(cls):
        return cls._scoped_engine

    def __init__(self, engine):
        self._old_engine = MigrationScope._scoped_engine
        self._old_cwd = os.getcwd()
        self._engine = engine

    def __enter__(self):
        MigrationScope._scoped_engine = self._engine
        os.chdir(APP_DIR.joinpath('internal/storage'))

    def __exit__(self, exc_type, exc_val, exc_tb):
        MigrationScope._scoped_engine = self._old_engine
        os.chdir(self._old_cwd)


def _run_command(engine, command: list):
    with MigrationScope(engine):
        alembic.config.main(argv=command)


def run_migrations(engine):
    _run_command(engine, ['upgrade', 'head'])


def make_migrations(engine):
    message = 'auto_' + datetime.now().strftime('%Y%m%d_%H%M%S')
    _run_command(engine, ['revision', '--autogenerate', '-m', message])


def rollback_all(engine):
    _run_command(engine, ['downgrade', 'base'])
