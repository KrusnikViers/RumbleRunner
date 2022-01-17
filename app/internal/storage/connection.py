import logging
from typing import Optional

from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

from app.bot.config import Config
from app.internal.storage.migrations import router


class DatabaseConnection:
    def __init__(self, configuration: Optional[Config], for_tests: bool = False):
        assert Config is not None or for_tests
        url = self._generate_db_url(configuration, for_tests)
        logging.info("Database path set to {}".format(url))
        self.engine = create_engine(url)
        self.make_session = sessionmaker(bind=self.engine)
        self.run_migrations()

    def run_migrations(self):
        logging.info('Running pending migrations')
        router.run_migrations(self.engine)

    @staticmethod
    def _generate_db_url(configuration: Optional[Config], for_tests: bool):
        if for_tests:
            return 'sqlite://'
        return "sqlite:///{}/storage.db".format(configuration.storage_dir)
