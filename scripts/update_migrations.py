from app.api.config import Config
from base.bot import Bot
from base.database.alembic.migrations import MigrationEngine
from base.database.connection import DatabaseConnection

Bot.set_logging_format()

# Provide db_path command line parameter for this script.
# Make sure that:
# - directory app/storage/migrations/versions exists
# - db_path directory exists as well
config = Config.create()
connection = DatabaseConnection.create(config.storage_dir)
migration_engine = MigrationEngine(connection.engine)
migration_engine.make_migrations()
