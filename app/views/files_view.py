import os
from http import HTTPStatus
from flask import request, Blueprint
from werkzeug.utils import secure_filename


FILES_DIRECTORY = os.environ.get('FILES_DIRECTORY')
ALLOWED_EXTENSIONS = os.environ.get('ALLOWED_EXTENSIONS') if os.environ.get('ALLOWED_EXTENSIONS') != None else ['png', 'jpg', 'gif']

bp_files = Blueprint("bp_files", __name__)

@bp_files.route("/files")
def list_files():
    """"
    Essa rota lista todas imagens todas as imagens contidas no banco de imagens.
    """
    result = []
    sub_directories = os.listdir(FILES_DIRECTORY)
    for directory in sub_directories:
        if os.path.isdir(f'{FILES_DIRECTORY}/{directory}') and directory in ALLOWED_EXTENSIONS:
            for file in os.listdir(f'{FILES_DIRECTORY}/{directory}'):
                result.append(file)
        else:
            ...

    return {'data': result}, HTTPStatus.OK


@bp_files.route("/files/<type>")
def list_files_by_type(type):
    """"
    Essa rota lista todas as imagens de uma extenção especifica contidas no bando de imagens.
    """
    if os.path.isdir(f'{FILES_DIRECTORY}/{type}'):
        result = os.listdir(f'{FILES_DIRECTORY}/{type}')
        return {'data': result}, HTTPStatus.OK
    else:
        return {'error': 'Not found'}, HTTPStatus.NOT_FOUND


def check_directory():
    """"
    Essa função verifica se o diretório que o usuário especificou no .env existe, assim como os subdiretórios,
    caso algum deles não exista, será criado.
    """
    if os.path.isdir(FILES_DIRECTORY):
        for extension in ALLOWED_EXTENSIONS:
            if os.path.isdir(f'{FILES_DIRECTORY}/{extension}'):
                ...
            else:
                path = os.path.join(FILES_DIRECTORY, extension)
                os.mkdir(path)
    else:
        directory = FILES_DIRECTORY
        parent_dir = "./"
        path = os.path.join(parent_dir, directory)
        os.mkdir(path)

        for extension in ALLOWED_EXTENSIONS:
            path = os.path.join(FILES_DIRECTORY, extension)
            os.mkdir(path)
