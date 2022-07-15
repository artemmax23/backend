import io
import os
import traceback
from flask import request
from flask_jwt_extended import jwt_required
from models.db_interface_class import DBInterface
from models.file_class import File
from repository.connect import Connect
from services.files_storage_system import FilesStorageSystem
from services.storage_interface import StorageInterface
from werkzeug.utils import secure_filename

system: StorageInterface = FilesStorageSystem.get_system()
db: DBInterface = Connect.connect()


@jwt_required()
def all() -> str:
    return db.all()


@jwt_required()
def one(file_id: int) -> str:
    try:
        return db.one(file_id)
    except BaseException:
        return traceback.format_exc()


@jwt_required()
def add() -> str:
    path: str = str(request.form['path'])
    file: io.bytesIO = request.files['file']
    comment: str = str(request.form['comment'])
    filename: str = secure_filename(file.filename)
    name: list = filename.split(".")
    info: int = os.fstat(file.fileno()).st_size
    try:
        path: str = system.add(file, path)
        db.insert(name[0], name[1], info, path, comment)
        return "True"
    except BaseException:
        return traceback.format_exc()


@jwt_required()
def delete(file_id: int) -> str:
    result: File = db.remove(file_id)
    if not (result is None):
        system.delete(result)
        return "True"
    else:
        return "Invalid file id!"
