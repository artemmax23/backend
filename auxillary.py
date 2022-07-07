import traceback
from flask import Blueprint, request, send_from_directory, g
import json
import os
import datetime

auxillary = Blueprint('auxillary', __name__)
UPLOAD_FOLDER = None
db = None

@auxillary.before_request
def before_request():
    global UPLOAD_FOLDER
    global db
    UPLOAD_FOLDER = g.get('upload_folder')
    db = g.get('db')

@auxillary.route("/find/", methods=['POST'])
def find():
    path = str(request.form['path'])
    return db.find(path)

@auxillary.route("/download/<fileId>", methods=['GET'])
def download(fileId):
    path = db.get_path(fileId)
    if path != None:
        return send_from_directory(directory=UPLOAD_FOLDER, path=path)
    else:
        return "Such file doesn't exist!"

@auxillary.route("/change/", methods=['POST'])
def change():
    try:
        fileId = int(request.form['fileId'])
        name =  str(request.form['name'])
        path =  str(request.form['path'])
        comment =  str(request.form['comment'])

        if (len(path) != 0) and (path[-1] != '/'):
            path += "/"

        temp = json.loads(db.one_info(fileId))
        old_path = UPLOAD_FOLDER + temp['path'] + temp['name'] + '.' + temp['extension']

        st = dict()
        new_path = UPLOAD_FOLDER

        if path != "":
            st['path'] = path
            new_path += path
            if not(os.path.exists(new_path)):
                os.makedirs(new_path)
        else:
            new_path += temp['path']

        if name != "":
            st['name'] = name
            new_path += name + '.' + temp['extension']
        else:
            new_path += temp['name'] + '.' + temp['extension']

        if comment != "":
            st['comment'] = comment

        st['updated_at'] = datetime.datetime.now()

        if new_path != old_path:
            os.replace(old_path, new_path)
            if len(os.listdir(UPLOAD_FOLDER + temp['path'])) == 0:
                os.removedirs(UPLOAD_FOLDER + temp['path'])

        db.update(fileId, st)
        return "True"
    except BaseException:
        return traceback.format_exc()

@auxillary.route("/sync/")
def sync():

    result = json.loads(db.all())
    db_paths = [UPLOAD_FOLDER + p['path'] + p['name'] + '.' + p['extension'] for p in result]
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
                db.insert([filename[0], filename[1], info[6], relative, ""])
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

        db.delete_by_path([name, extension, path])

    return "True"