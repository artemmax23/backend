from controllers.main_controller import all, one, add, delete
from flask import Blueprint, request, send_from_directory

main = Blueprint('main', __name__)

main.route("/all/")(all)
main.route("/one/<file_id>", methods=['GET'])(one)
main.route("/add/", methods=['POST'])(add)
main.route("/delete/<file_id>", methods=['GET'])(delete)
