from controllers.main_controller import all, one, add, delete
from flask import Blueprint, request, send_from_directory

main_bp = Blueprint('main_bp', __name__)

main_bp.route("/all/")(all)
main_bp.route("/one/<file_id>", methods=['GET'])(one)
main_bp.route("/add/", methods=['POST'])(add)
main_bp.route("/delete/<file_id>", methods=['GET'])(delete)
