from .postgres_db_class import PostgresDb


class Connect:
    db = staticmethod(None)

    @staticmethod
    def connect():
        if Connect.db is None:
            Connect.db = PostgresDb()
        return Connect.db
