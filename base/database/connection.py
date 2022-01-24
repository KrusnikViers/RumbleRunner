import logging

from sqlalchemy.engine import create_engine, Engine
from sqlalchemy.orm import sessionmaker

from app.api.config import Config
from base.database.alembic.migrations import MigrationEngine


class DatabaseConnection:
    def __init__(self, engine: Engine):
        self.engine = engine
        self.make_session = sessionmaker(bind=self.engine)

    @staticmethod
    def create(storage_dir: str) -> 'DatabaseConnection':
        url = "sqlite:///{}/storage.db".format(storage_dir)
        return DatabaseConnection._create_from_url(url)

    @staticmethod
    def create_for_tests() -> 'DatabaseConnection':
        return DatabaseConnection._create_from_url('sqlite://')

    # Private methods
    @staticmethod
    def _create_from_url(db_url: str) -> 'DatabaseConnection':
        logging.info("Database path set to {}".format(db_url))
        engine = create_engine(db_url)
        logging.info('Running pending migrations')
        MigrationEngine(engine).run_migrations()
        return DatabaseConnection(engine)
