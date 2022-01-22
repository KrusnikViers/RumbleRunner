import os
import sys

from app.api.info import APP_DIR
from base.database.alembic.migrations import MigrationEngine
from tests.utils import InBotTestCase


class PrintSuppressor:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


class TestMigrations(InBotTestCase):
    def test_connection(self):
        self.assertIsNotNone(self.connection.engine)
        with self.connection.engine.connect():
            pass

    def test_nothing_more_to_migrate(self):
        migrations_dir = APP_DIR.joinpath('migrations')

        # Generate new migration and make sure it was generated.
        old_migrations_list = sorted(os.listdir(migrations_dir))
        with PrintSuppressor():
            MigrationEngine(self.connection.engine).make_migrations()
        new_migrations = [file for file in os.listdir(migrations_dir) if file not in old_migrations_list]
        self.assertEqual(1, len(new_migrations))

        # Get migration file contents, removing migration file itself.
        migration_file_path = str(migrations_dir.joinpath(new_migrations[0]))
        with open(migration_file_path, 'r') as migration_file:
            migration_contents = migration_file.read().replace('\n', ' ').split()
        os.remove(migration_file_path)

        # Check that migration body contains |pass| for both upgrade and downgrade methods.
        commands_sequence = ['upgrade():', 'pass', 'downgrade():', 'pass']
        self.assertEqual(commands_sequence,
                         [command for command in migration_contents if command in commands_sequence])

    def test_complete_upgrade_downgrade(self):
        engine = MigrationEngine(self.connection.engine)
        engine.rollback_all()
        engine.run_migrations()
