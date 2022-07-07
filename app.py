import traceback
from flask import Flask, request, g
from werkzeug.utils import secure_filename
import os
from auxillary import auxillary
from DataSources.my_sql_db_class import MySqlDb

app = Flask(__name__)
app.register_blueprint(auxillary)
db = MySqlDb()

UPLOAD_FOLDER = 'D:/downloads/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

@app.before_request
def before_request():
    if not hasattr(g, 'upload_folder'):
        g.upload_folder = app.config['UPLOAD_FOLDER']
        g.db = db

@app.route("/all/")
def home():
    return db.all()

@app.route("/oneinfo/<file_id>", methods=['GET'])
def one_info(file_id):
    try:
        return db.one_info(file_id)
    except BaseException:
        return traceback.format_exc()

@app.route("/addfile/", methods=['POST'])
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
        if (len(path) != 0) and not(os.path.exists(app.config['UPLOAD_FOLDER'] + path)):
            os.makedirs(app.config['UPLOAD_FOLDER'] + path)
        file.save(app.config['UPLOAD_FOLDER'] + path + filename)
        info = os.stat(app.config['UPLOAD_FOLDER'] + path + filename)
        db.insert([name[0], name[1], info[6], path, comment])
        return "True"
    except BaseException:
        return traceback.format_exc()

@app.route("/deletefile/<file_id>", methods=['GET'])
def delete(file_id):
    result = db.remove(file_id)
    if (result != None):
        os.remove(app.config['UPLOAD_FOLDER'] + result.path + result.name + '.' + result.extension)
        if len(os.listdir(app.config['UPLOAD_FOLDER'] + result.path)) == 0:
            os.removedirs(app.config['UPLOAD_FOLDER'] + result.path)
        return "True"
    else:
        return "Invalid file id!"

if __name__ == "__main__":
    app.run()