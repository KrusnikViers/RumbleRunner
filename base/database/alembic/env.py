from alembic import context

from base.models.base import BaseDBModel
from base.database.alembic.migrations import MigrationEngine, MigrationScope

# This forces all models to be defined, and therefore to be added in the Base model metadata.
from app.models.all import *
from base.models.all import *

target_metadata = BaseDBModel.metadata
with MigrationScope.current_engine().connect() as connection:
    context.configure(connection=connection, target_metadata=target_metadata, render_as_batch=True)
    with context.begin_transaction():
        context.run_migrations()
