import json
import traceback
from flask import request
from repository.connect import Connect
from services.files_storage_system import FilesStorageSystem

system = FilesStorageSystem.get_system()
db = Connect.connect()


def find():
    path = str(request.form['path'])
    return db.find(path)


def download(file_id):
    path = db.get_path(file_id)
    if path != None:
        return system.download(path)
    else:
        return "Such file doesn't exist!"


def update():
    file_id = int(request.form['file_id'])
    name = str(request.form['name'])
    path = str(request.form['path'])
    comment = str(request.form['comment'])

    try:
        temp = json.loads(db.one(file_id))
        st = system.update(name, path, temp['extension'], temp['name'], temp['path'])
        if comment != "":
            st['comment'] = comment
        else:
            st['comment'] = temp['comment']
        db.update(file_id, st['name'], st['path'], st['comment'])
        return "True"
    except BaseException:
        return traceback.format_exc()


def sync():
    insert_list, delete_list = system.sync(db.all())
    for p in insert_list:
        db.insert(p['name'], p['extension'], p['size'], p['path'], p['comment'])

    for p in delete_list:
        db.delete_by_path(p['name'], p['extension'], p['path'])

    return "True"
