from alembic import context

from app.internal.storage.migrations import router
from app.internal.storage.models.base import BaseDBModel

# This forces all models to be defined, and therefore to be added in the Base model metadata.
from app.bot.models.all import *
from app.internal.storage.models.all import *

target_metadata = BaseDBModel.metadata
with router.MigrationScope.current_engine().connect() as connection:
    context.configure(connection=connection, target_metadata=target_metadata, render_as_batch=True)
    with context.begin_transaction():
        context.run_migrations()
