class MigrationScope:
    _engine = None

    @classmethod
    def engine(cls):
        assert cls._engine is not None
        return cls._engine

    def __init__(self, engine):
        self.old = None
        self.engine = engine

    def __enter__(self):
        self.old = MigrationScope._engine
        MigrationScope._engine = self.engine

    def __exit__(self, exc_type, exc_val, exc_tb):
        MigrationScope._engine = self.old
