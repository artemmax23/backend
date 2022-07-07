from DBInterfaceClass import DBInterface
from fileClass import File, Session
import json

class MySqlDb(DBInterface):
    session = Session()

    def all(self):
        result = self.session.query(File).all()
        data = [{'id': p.id, 'name': p.name, 'extension': p.extension, 'size': p.size,
                 'path': p.path, 'created_at': p.created_at.__str__(),
                 'updated_at': p.updated_at.__str__(),
                 'comment': p.comment} for p in result]
        return json.dumps(data)

    def one_info(self, file_id):
        result = self.session.query(File).filter(File.id == file_id).first()
        data = {'id': result.id, 'name': result.name, 'extension': result.extension, 'size': result.size,
                'path': result.path, 'created_at': result.created_at.__str__(),
                'updated_at': result.updated_at.__str__(),
                'comment': result.comment}
        return json.dumps(data)

    def insert(self, data):
        if self.session.query(File).filter(File.name == data[0]).filter(
                File.extension == data[1]).filter(
                File.path == data[3]).first() != None:
             raise Exception('Such file exist!')
        file = File(data[0], data[1], data[2], data[3], data[4])
        self.session.add(file)
        self.session.commit()

    def remove(self, file_id):
        result = self.session.query(File).filter(File.id == file_id).first()
        if (result != None):
            self.session.delete(result)
            self.session.commit()
        return result

    def find(self, path):
        path = "%{}%".format(path)
        result = self.session.query(File).filter(File.path.like(path)).all()
        if result:
            data = [{'name': p.name, 'extension': p.extension, 'size': p.size,
                     'path': p.path, 'created_at': p.created_at.__str__(),
                     'updated_at': p.updated_at.__str__(),
                     'comment': p.comment} for p in result]
            return json.dumps(data)
        else:
            return "Such files doesn't exist!"

    def update(self, file_id, data):
        self.session.query(File).filter(File.id == file_id).update(data)
        self.session.commit()

    def get_path(self, file_id):
        result = self.session.query(File).filter(File.id == file_id).first()
        if result == None:
            return result
        else:
            return result.path + result.name + '.' + result.extension

    def delete_by_path(self, path):
        result = self.session.query(File).filter(File.name == path[0]).filter(File.extension == path[1]).filter(
            File.path == path[2]).first()
        self.session.delete(result)
        self.session.commit()