from flask import Flask, request, g
from werkzeug.utils import secure_filename
from fileClass import Session, File
import os
import json
from auxillary import auxillary

app = Flask(__name__)
app.register_blueprint(auxillary)

UPLOAD_FOLDER = 'D:/downloads/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

session = Session()

@app.before_request
def before_request():
    if not hasattr(g, 'upload_folder'):
        g.upload_folder = app.config['UPLOAD_FOLDER']
    if not hasattr(g, 'session'):
        g.session = session

@app.route("/")
def home():
    result = session.query(File).all()
    data = [{'name': p.name, 'extension': p.extension, 'size': p.size,
             'path': p.path, 'created_at': p.created_at.__str__(),
             'updated_at': p.updated_at.__str__(),
             'comment': p.comment} for p in result]
    return json.dumps(data)

@app.route("/oneinfo/<fileId>", methods=['GET'])
def oneinfo(fileId):
    result = session.query(File).filter(File.id == fileId).first()
    data = {'name': result.name, 'extension': result.extension, 'size': result.size,
             'path': result.path, 'created_at': result.created_at.__str__(),
              'updated_at': result.updated_at.__str__(),
             'comment': result.comment}
    return json.dumps(data)

@app.route("/addfile/", methods=['POST'])
def add():
    path = str(request.form['path'])
    if (len(path) != 0) and (path[-1] != '/'):
        path += "/"
    if (len(path) != 0):
        os.makedirs(app.config['UPLOAD_FOLDER'] + path)
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(app.config['UPLOAD_FOLDER'] + path + filename)
    info = os.stat(app.config['UPLOAD_FOLDER'] + path + filename)
    name = filename.split(".")
    comment = str(request.form['comment'])
    if session.query(File).filter(File.name == name[0]).filter(File.extension == name[1]).filter(File.path == path).first() != None:
        return "Such file exist"
    file = File(name[0], name[1], info[6], path, comment)
    session.add(file)
    session.commit()

    return "True"

@app.route("/deletefile/<fileId>", methods=['GET'])
def delete(fileId):
    result = session.query(File).filter(File.id == fileId).first()
    if (result != None):
        os.remove(app.config['UPLOAD_FOLDER'] + result.path + result.name + '.' + result.extension)
        if len(os.listdir(app.config['UPLOAD_FOLDER'] + result.path)) == 0:
            os.removedirs(app.config['UPLOAD_FOLDER'] + result.path)
        session.delete(result)
        session.commit()

    return "True"