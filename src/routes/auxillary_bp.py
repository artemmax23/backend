from controllers.auxillary_controller import find, download, update, sync
from flask import Blueprint

auxillary_bp = Blueprint('auxillary_bp', __name__)

auxillary_bp.route("/find/", methods=['POST'])(find)
auxillary_bp.route("/download/<file_id>", methods=['GET'])(download)
auxillary_bp.route("/update/", methods=['POST'])(update)
auxillary_bp.route("/sync/")(sync)
