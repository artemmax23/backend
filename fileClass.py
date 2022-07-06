from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, TIMESTAMP
import datetime
from sqlalchemy.orm import mapper, sessionmaker

engine = create_engine('mysql://root:123@localhost:3306/filestorage', echo=False)
Session = sessionmaker(bind=engine)

metadata = MetaData()
files_table = Table('files', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(100)),
    Column('extension', String(4)),
    Column('size', Integer),
    Column('path', String(200)),
    Column('created_at', TIMESTAMP),
    Column('updated_at', TIMESTAMP),
    Column('comment', String(200))
)

metadata.create_all(engine)

class File(object):
    def __init__(self, name, extension, size, path, comment):
        self.name = name
        self.extension = extension
        self.size = size
        self.path = path
        self.comment = comment
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()

mapper(File, files_table)