from typing import Optional

from sqlalchemy import orm

from base.database.connection import DatabaseConnection


class SessionScope:
    @classmethod
    def session(cls) -> orm.Session:
        assert cls._session is not None
        return cls._session

    @classmethod
    def commit(cls):
        cls.session().commit()

    # Private methods
    _session: Optional[orm.Session] = None

    def __init__(self, connection: DatabaseConnection):
        self.connection = connection
        self.session: Optional[orm.Session] = None
        self.old_session: Optional[orm.Session] = None

    def __enter__(self):
        self.old_session = SessionScope._session
        self.session = self.connection.make_session()
        SessionScope._session = self.session
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.close()
        SessionScope._session = self.old_session
