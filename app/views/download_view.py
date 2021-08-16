import os
import shutil
from http import HTTPStatus
from flask import request, Blueprint, send_from_directory


FILES_DIRECTORY = os.environ.get('FILES_DIRECTORY')

bp_download = Blueprint("bp_download", __name__)

@bp_download.route("/download/<file_name>")
def download(file_name):
    """"
    Essa rota faz o download do um arquivo especifico.
    """
    file_extension = file_name.split('.')[-1].lower()
    path = f'../{FILES_DIRECTORY}/{file_extension}/'
    return  send_from_directory(path, file_name, as_attachment=True), HTTPStatus.OK

@bp_download.route("/download-zip")
def download_dir_as_zip():
    """"
    Essa rota faz o download de um diretório especifico zipado.
    """
    file_type = request.args.get('file_type')
    compression_rate = request.args.get('compression_rate')

    path = f'{FILES_DIRECTORY}/{file_type}/'
    if len(os.listdir(path)) > 0:
        os.system(f'cd {FILES_DIRECTORY}; zip -{compression_rate} -r {file_type}.zip {file_type}; mv {file_type}.zip /tmp')
        file_name = f'{file_type}.zip'
        return send_from_directory('/tmp', file_name, as_attachment=True), HTTPStatus.OK
    else:
        return {"error": "Not found"}, HTTPStatus.NOT_FOUND

    