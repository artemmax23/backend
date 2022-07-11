from .postgres_db_class import PostgresDb


class Connect:
    def __init__(self):
        pass

    db = staticmethod(None)

    @staticmethod
    def connect():
        if Connect.db is None:
            Connect.db = PostgresDb()
        return Connect.db
