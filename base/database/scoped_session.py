from sqlalchemy import orm

from base.database.connection import DatabaseConnection


class ScopedSession:
    def __init__(self, connection: DatabaseConnection):
        self.session: orm.Session = connection.make_session()

    def __enter__(self):
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.close()
