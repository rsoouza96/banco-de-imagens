import os
from http import HTTPStatus
from flask import request, Blueprint
from werkzeug.utils import secure_filename


FILES_DIRECTORY = os.environ.get('FILES_DIRECTORY')
MAX_CONTENT_LENGTH = os.environ.get('MAX_CONTENT_LENGTH') if os.environ.get('MAX_CONTENT_LENGTH') != None else 1
ALLOWED_EXTENSIONS = os.environ.get('ALLOWED_EXTENSIONS') if os.environ.get('ALLOWED_EXTENSIONS') != None else ['png', 'jpg', 'gif']

bp_upload = Blueprint("bp_upload", __name__)

@bp_upload.route("/upload", methods=["POST"])
def upload():
    """"
    Essa rota recebe um arquivo de um campo "file", a partir disso:
    - Verifica se o tipo de arquivo é válido;
    - Verifica se já existe um arquivo com o mesmo nome;
    - Verifica se o tamanho do arquivo é aceitável;
    - Se todas as verificações anteriores estiverem OK, salva o arquivo no seu devido subdiretório.
    """
    file = request.files['file']
    filename = file.filename
    file_extension = filename.split('.')[-1].lower()

    if(file_extension in ALLOWED_EXTENSIONS):
        path = f'{FILES_DIRECTORY}/{file_extension}'
        directory = os.listdir(path)
        if(filename not in directory):
            file_read = file.read()
            file_size = len(file_read)/1024

            if(file_size < (int(MAX_CONTENT_LENGTH)*1024)):
                save_path = os.path.join(os.getcwd(), path, secure_filename(file.filename))
                file.save(save_path)
                return {'data': 'Created'}, HTTPStatus.CREATED
            else:
                return {'error': 'Payload Too Large'}, HTTPStatus.REQUEST_ENTITY_TOO_LARGE
        else:
            return {'error': 'Conflict'}, HTTPStatus.CONFLICT
    else:
        return {'error': 'Unsupported Media Type'}, HTTPStatus.UNSUPPORTED_MEDIA_TYPE