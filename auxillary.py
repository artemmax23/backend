from flask import Blueprint, request,  session, send_from_directory, g
from fileClass import File
import json
import os
import datetime

auxillary = Blueprint('auxillary', __name__)
UPLOAD_FOLDER = None
session = None

@auxillary.before_request
def before_request():
    global UPLOAD_FOLDER
    global session
    UPLOAD_FOLDER = g.get('upload_folder')
    session = g.get('session')

@auxillary.route("/")
def find():
    path = str(request.form['path'])
    path = "%{}%".format(path)
    result = session.query(File).filter(File.path.like(path)).all()
    data = [{'name': p.name, 'extension': p.extension, 'size': p.size,
             'path': p.path, 'created_at': p.created_at.__str__(),
             'updated_at': p.updated_at.__str__(),
             'comment': p.comment} for p in result]

    return json.dumps(data)

@auxillary.route("/download/<fileId>", methods=['GET'])
def download(fileId):
    result = session.query(File).filter(File.id == fileId).first()
    return send_from_directory(directory=UPLOAD_FOLDER, path=result.path + result.name + '.' + result.extension)

@auxillary.route("/change/", methods=['POST'])
def change():
    fileId = int(request.form['fileId'])
    name =  str(request.form['name'])
    path =  str(request.form['path'])
    comment =  str(request.form['comment'])

    if (len(path) != 0) and (path[-1] != '/'):
        path += "/"

    temp = session.query(File).filter(File.id == fileId).first()
    old_path = UPLOAD_FOLDER + temp.path + temp.name + '.' + temp.extension

    st = dict()
    new_path = UPLOAD_FOLDER

    if path != "":
        st['path'] = path
        new_path += path
        os.makedirs(new_path)
    else:
        new_path += temp.path

    if name != "":
        st['name'] = name
        new_path += name + '.' + temp.extension
    else:
        new_path += temp.name + '.' + temp.extension

    if comment != "":
        st['comment'] = comment

    st['updated_at'] = datetime.datetime.now()

    if new_path != old_path:
        os.replace(old_path, new_path)
        if len(os.listdir(UPLOAD_FOLDER + temp.path)) == 0:
            os.removedirs(UPLOAD_FOLDER + temp.path)

    session.query(File).filter(File.id == fileId).update(st)
    session.commit()

    return "True"

@auxillary.route("/sync/")
def sync():

    result = session.query(File).all()
    db_paths = [UPLOAD_FOLDER + p.path + p.name + '.' + p.extension for p in result]
    cnt = UPLOAD_FOLDER.count('/')

    for address, dirs, files in os.walk(UPLOAD_FOLDER):
        for name in files:
            path = os.path.join(address, name)
            path = path.replace('\\', '/')
            address = address.replace('\\', '/')
            if not(path in db_paths):
                filename = name.split('.')
                info = os.stat(path)
                relative = address.split('/', cnt)[cnt] + '/'
                file = File(filename[0], filename[1], info[6], relative, "")
                session.add(file)
                session.commit()
            else:
                db_paths.remove(path)

    for p in db_paths:
        relative = p.split('/', cnt)
        relative.reverse()
        fullname, path = relative[0][::-1].split('/', 1)
        path = path[::-1]
        fullname = fullname[::-1]
        path += '/'
        if len(os.listdir(UPLOAD_FOLDER + path)) == 0:
            os.removedirs(UPLOAD_FOLDER + path)
        name, extension = fullname.split('.', 1)
        result = session.query(File).filter(File.name == name).filter(File.extension == extension).filter(File.path == path).first()
        session.delete(result)
        session.commit()

    return "True"