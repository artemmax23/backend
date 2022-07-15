from models.db_interface_class import DBInterface

from .postgres_db_class import PostgresDb


class Connect:
    def __init__(self):
        pass

    db: DBInterface = staticmethod(None)

    @staticmethod
    def connect() -> DBInterface:
        if Connect.db is None:
            Connect.db = PostgresDb()
        return Connect.db
