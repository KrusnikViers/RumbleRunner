from alembic import context

from base.models.base import BaseDBModel
from base.database.alembic.migration_scope import MigrationScope

# This forces all models to be defined, and therefore to be added in the Base model metadata.
from app.models import *
from base.models import *

target_metadata = BaseDBModel.metadata
with MigrationScope.engine().connect() as connection:
    context.configure(connection=connection, target_metadata=target_metadata, render_as_batch=True)
    with context.begin_transaction():
        context.run_migrations()
