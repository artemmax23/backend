import io
import json
import traceback
from flask import request, send_file
from flask_jwt_extended import jwt_required
from models.db_interface_class import DBInterface
from models.file_class import File
from repository.connect import Connect
from services.files_storage_system import FilesStorageSystem
from services.storage_interface import StorageInterface

system: StorageInterface = FilesStorageSystem.get_system()
db: DBInterface = Connect.connect()


@jwt_required()
def find() -> str:
    path: str = str(request.form['path'])
    return db.find(path)


@jwt_required()
def download(file_id: int) -> str:
    file: dict = json.loads(db.one(file_id))
    if not (file is None):
        sd_file: io.bytesIO = system.download(file['name'], file['extension'], file['path'])
        sd_file.seek(0)
        return send_file(
            sd_file,
            mimetype='txt/plain',
            download_name=(file['name'] + '.' + file['extension']))
    else:
        return "Such file doesn't exist!"


@jwt_required()
def update() -> str:
    file_id: int = int(request.form['file_id'])
    name: str = str(request.form['name'])
    path: str = str(request.form['path'])
    comment: str = str(request.form['comment'])

    try:
        temp: dict = json.loads(db.one(file_id))
        path: str = system.update(name, path, temp['extension'], temp['name'], temp['path'])
        if name == "":
            name = temp['name']
        if comment == "":
            comment = temp['comment']
        db.update(file_id, name, path, comment)
        return "True"
    except BaseException:
        return traceback.format_exc()


@jwt_required()
def sync() -> str:
    insert_list: list = []
    delete_list: list = []

    insert_list, delete_list = system.sync(db.all())
    for p in insert_list:
        db.insert(p['name'], p['extension'], p['size'], p['path'], p['comment'])

    for p in delete_list:
        db.delete_by_path(p['name'], p['extension'], p['path'])

    return "True"
