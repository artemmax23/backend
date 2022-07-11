import datetime
import json
import os
import traceback
from flask import Blueprint, request, send_from_directory, g
from flask import Flask, request, g
from werkzeug.utils import secure_filename
from .data_sources.postgres_db_class import PostgresDb

main = Blueprint('main', __name__)
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'D:/downloads')
db = PostgresDb()


@main.route("/all/")
def home():
    return db.all()


@main.route("/oneinfo/<file_id>", methods=['GET'])
def one_info(file_id):
    try:
        return db.one_info(file_id)
    except BaseException:
        return traceback.format_exc()


@main.route("/addfile/", methods=['POST'])
def add():
    path = str(request.form['path'])
    if (len(path) != 0) and (path[-1] != '/'):
        path += "/"
    file = request.files['file']
    filename = secure_filename(file.filename)
    comment = str(request.form['comment'])
    try:
        name = filename.split(".")
        if len(name[1]) > 4:
            return "Invalid file extension!"
        if (len(path) != 0) and not (os.path.exists(UPLOAD_FOLDER + path)):
            os.makedirs(UPLOAD_FOLDER + path)
        else:
            os.makedirs(UPLOAD_FOLDER)
        file.save(UPLOAD_FOLDER + path + filename)
        info = os.stat(UPLOAD_FOLDER + path + filename)
        db.insert([name[0], name[1], info[6], path, comment])
        return "True"
    except BaseException:
        return traceback.format_exc()


@main.route("/deletefile/<file_id>", methods=['GET'])
def delete(file_id):
    result = db.remove(file_id)
    if (result != None):
        os.remove(UPLOAD_FOLDER + result.path + result.name + '.' + result.extension)
        if len(os.listdir(UPLOAD_FOLDER + result.path)) == 0:
            os.removedirs(UPLOAD_FOLDER + result.path)
        return "True"
    else:
        return "Invalid file id!"
