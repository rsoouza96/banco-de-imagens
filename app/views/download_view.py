import os
from flask import request, Blueprint
from app.kenzie.image import download_file, download_zip_file

bp_download = Blueprint("bp_download", __name__)

@bp_download.route("/download/<file_name>")
def download(file_name):
    return download_file(file_name)

@bp_download.route("/download-zip")
def download_dir_as_zip():
    file_type = request.args.get('file_type')
    compression_rate = request.args.get('compression_rate')
    return download_zip_file(file_type, compression_rate)