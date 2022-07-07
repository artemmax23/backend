from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP
import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql://root:123@localhost:3306/filestorage', echo=False)
Session = sessionmaker(bind=engine)

Base = declarative_base()
class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    extension = Column(String(4))
    size = Column(Integer)
    path = Column(String(200))
    created_at = Column(TIMESTAMP, default=datetime.datetime.now())
    updated_at = Column(TIMESTAMP, default=datetime.datetime.now())
    comment = Column(String(200))

    def __init__(self, name, extension, size, path, comment):
        self.name = name
        self.extension = extension
        self.size = size
        self.path = path
        self.comment = comment

Base.metadata.create_all(engine)