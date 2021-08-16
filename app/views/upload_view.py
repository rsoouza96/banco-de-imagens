from flask import request, Blueprint
from ..kenzie.image import upload_file


bp_upload = Blueprint("bp_upload", __name__)


@bp_upload.route("/upload", methods=["POST"])
def upload():
    file = request.files['file']
    return upload_file(file)