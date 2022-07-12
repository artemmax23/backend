from controllers.auxillary_controller import find, download, update, sync
from flask import Blueprint

auxillary = Blueprint('auxillary', __name__)

auxillary.route("/find/", methods=['POST'])(find)

auxillary.route("/download/<file_id>", methods=['GET'])(download)

auxillary.route("/update/", methods=['POST'])(update)

auxillary.route("/sync/")(sync)
