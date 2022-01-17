from app.bot.config import Config
from app.internal.log import global_logging_init
from app.internal.storage.connection import DatabaseConnection
from app.internal.storage.migrations import router

global_logging_init()

# Provide db_path command line parameter for this script.
# Make sure that:
# - directory app/storage/migrations/versions exists
# - db_path directory exists as well
config = Config.get()
connection = DatabaseConnection(config)

router.make_migrations(connection.engine)
