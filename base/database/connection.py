import logging
from typing import Optional

from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import Config
from base.database.alembic.migrations import MigrationEngine


class DatabaseConnection:
    def __init__(self, configuration: Optional[Config], for_tests: bool = False):
        assert Config is not None or for_tests
        url = self.create_database_url(configuration, for_tests)
        logging.info("Database path set to {}".format(url))
        self.engine = create_engine(url)
        self.make_session = sessionmaker(bind=self.engine)
        logging.info('Running pending migrations')
        MigrationEngine(self.engine).run_migrations()

    @staticmethod
    def create_database_url(configuration: Optional[Config], for_tests: bool):
        if for_tests:
            return 'sqlite://'
        return "sqlite:///{}/storage.db".format(configuration.storage_dir)
