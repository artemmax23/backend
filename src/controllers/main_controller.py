import os
import traceback
from flask import request
from repository.connect import Connect
from services.files_storage_system import FilesStorageSystem
from werkzeug.utils import secure_filename

system = FilesStorageSystem.get_system()
db = Connect.connect()


def all():
    return db.all()


def one(file_id: int):
    try:
        return db.one(file_id)
    except BaseException:
        return traceback.format_exc()


def add():
    path = str(request.form['path'])
    file = request.files['file']
    comment = str(request.form['comment'])
    filename = secure_filename(file.filename)
    name = filename.split(".")
    info = os.fstat(file.fileno()).st_size
    try:
        path = system.add(file, path, comment)
        db.insert(name[0], name[1], info, path, comment)
        return "True"
    except BaseException:
        return traceback.format_exc()


def delete(file_id: int):
    result = db.remove(file_id)
    if not (result is None):
        system.delete(file_id)
        return "True"
    else:
        return "Invalid file id!"
