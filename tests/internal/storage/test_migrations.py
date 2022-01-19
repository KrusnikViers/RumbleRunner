import os
import sys

from app.bot.info import APP_DIR
from app.internal.storage.migrations import router
from app.internal.storage.scoped_session import ScopedSession
from app.internal.storage.models.all import TelegramUser
from tests.base import InBotTestCase


class PrintSuppressor:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


class TestDBCommon(InBotTestCase):
    def test_connection(self):
        self.assertIsNotNone(self.connection.engine)
        with self.connection.engine.connect():
            pass

    def test_nothing_more_to_migrate(self):
        migrations_dir = APP_DIR.joinpath('bot', 'migrations')

        # Generate new migration and make sure it was generated.
        old_migrations_list = sorted(os.listdir(migrations_dir))
        with PrintSuppressor():
            router.make_migrations(self.connection.engine)
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
        router.rollback_all(self.connection.engine)
        router.run_migrations(self.connection.engine)

    def test_session_rollback(self):
        with self.assertRaises(Exception):
            with ScopedSession(self.connection) as session:
                new_user = TelegramUser(tg_id=0, first_name='test')
                session.add(new_user)
                self.assertEqual(1, len(session.query(TelegramUser).all()))
                session.flush()
                raise Exception

        # Make sure, that after exception inside session, session will be rolled back.
        with ScopedSession(self.connection) as session:
            self.assertEqual(0, len(session.query(TelegramUser).all()))
