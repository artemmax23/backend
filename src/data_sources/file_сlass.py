import datetime
import os

from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

user = os.getenv('DB_USER', 'root')
host = os.getenv('DB_HOST', 'localhost')
password = os.getenv('DB_PASSWORD', 'root')
database = os.getenv('DB_NAME', 'filestorage')
port = os.getenv('DB_PORT', '5432')

engine = create_engine(f"postgresql+pg8000://{user}:{password}@{host}:{port}/{database}", echo=False)
Session = sessionmaker(bind=engine)

Base = declarative_base()


class File(Base):
    __tablename__ = "files"
    id: int
    name: str
    extension: str
    size: int
    path: str
    created_at: datetime
    updated_at: datetime
    comment: str

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    extension = Column(String(4))
    size = Column(Integer)
    path = Column(String(200))
    created_at = Column(TIMESTAMP, default=datetime.datetime.now())
    updated_at = Column(TIMESTAMP, default=datetime.datetime.now())
    comment = Column(String(200))

    def __init__(self, name: str, extension: str,
                 size: int, path: str, comment: str):
        self.name = name
        self.extension = extension
        self.size = size
        self.path = path
        self.comment = comment


Base.metadata.create_all(engine)
