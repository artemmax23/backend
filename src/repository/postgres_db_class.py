import datetime
import json
from models.db_interface_class import DBInterface
from models.file_class import File, Session


class PostgresDb(DBInterface):
    session = Session()

    def all(self) -> str:
        result: list = self.session.query(File).all()
        data: list = [{'id': p.id, 'name': p.name, 'extension': p.extension, 'size': p.size,
                       'path': p.path, 'created_at': p.created_at.__str__(),
                       'updated_at': p.updated_at.__str__(),
                       'comment': p.comment} for p in result]
        return json.dumps(data, ensure_ascii=False)

    def one(self, file_id: int) -> str:
        result: File = self.session.query(File).filter(File.id == int(file_id)).first()
        data: dict = {'id': result.id, 'name': result.name, 'extension': result.extension, 'size': result.size,
                      'path': result.path, 'created_at': result.created_at.__str__(),
                      'updated_at': result.updated_at.__str__(),
                      'comment': result.comment}
        return json.dumps(data, ensure_ascii=False)

    def insert(self, name: str, extension: str,
               size: int, path: str, comment: str):
        if not (self.session.query(File).filter(File.name == name).filter(
                File.extension == extension).filter(
            File.path == path).first() is None):
            raise Exception('Such file exist!')
        file: File = File(name, extension, size, path, comment)
        self.session.add(file)
        self.session.commit()

    def remove(self, file_id: int) -> File:
        result: File = self.session.query(File).filter(File.id == int(file_id)).first()
        if result is not None:
            self.session.delete(result)
            self.session.commit()
        return result

    def find(self, path: str) -> str:
        path: str = "%{}%".format(path)
        result: list = self.session.query(File).filter(File.path.like(path)).all()
        if result:
            data: list = [{'id': p.id, 'name': p.name, 'extension': p.extension, 'size': p.size,
                           'path': p.path, 'created_at': p.created_at.__str__(),
                           'updated_at': p.updated_at.__str__(),
                           'comment': p.comment} for p in result]
            return json.dumps(data, ensure_ascii=False)
        else:
            return "Such files doesn't exist!"

    def update(self, file_id: int, name: str,
               path: str, comment: str):
        data: dict = {'name': name, 'path': path, 'comment': comment, 'updated_at': datetime.datetime.now()}
        self.session.query(File).filter(File.id == int(file_id)).update(data)
        self.session.commit()

    def delete_by_path(self, name: str, extension: str, path: str):
        result: File = self.session.query(File).filter(File.name == name).filter(File.extension == extension).filter(
            File.path == path).first()
        self.session.delete(result)
        self.session.commit()
