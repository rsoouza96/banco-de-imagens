import os
import shutil
from http import HTTPStatus
from flask import send_from_directory
from werkzeug.utils import secure_filename


FILES_DIRECTORY = os.environ.get('FILES_DIRECTORY')
MAX_CONTENT_LENGTH = os.environ.get('MAX_CONTENT_LENGTH') if os.environ.get('MAX_CONTENT_LENGTH') != None else 1
ALLOWED_EXTENSIONS = os.environ.get('ALLOWED_EXTENSIONS') if os.environ.get('ALLOWED_EXTENSIONS') != None else ['png', 'jpg', 'gif']


def download_file(file_name):
    """
    Essa função recebe o nome do arquivo que o usuário está tentando baixar,
    busca o local onde o arquivo está e faz  o download.
    """

    file_extension = file_name.split('.')[-1].lower()
    path = f'../{FILES_DIRECTORY}/{file_extension}/'
    return send_from_directory(path, file_name, as_attachment=True), HTTPStatus.OK


def download_zip_file(file_type, compression_rate):
    """
    Essa função recebe o tipo do arquivo e o nível de compressão,
     a partir disso executa uma série de comandos no terminal, primeiro localiza o diretório,
     zipa ele e depois move para a pasta /tmp, depois de rodar esses comandos, é feito o download.
    """
    path = f'{FILES_DIRECTORY}/{file_type}/'
    if len(os.listdir(path)) > 0:
        os.system(f'cd {FILES_DIRECTORY}; zip -{compression_rate} -r {file_type}.zip {file_type}; mv {file_type}.zip /tmp')
        file_name = f'{file_type}.zip'
        return send_from_directory('/tmp', file_name, as_attachment=True), HTTPStatus.OK
    else:
        return {"error": "Not found"}, HTTPStatus.NOT_FOUND


def upload_file(file):
    """
    Essa função recebe um arquivo como parametro, que deve ser enviado por meio de um
    formulário, por um campo nomeado "file", com o valor sendo o arquivo a ser enviado.
    Depois de receber o arquivo, ele passará por uma série de verificações:
    -Se a extenção dela é permitida;
    -Se já existe um arquivo de mesmo nome armazenado;
    -Se o tamanho do arquivo é válido.
    Caso ele não passe em alguma dessas validações a função retorna seu respectivo erro,
    caso contrário, o upload será feito.
    """
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


def list_all_files():
    """
    Essa função retorna o nome de todos os arquivos que foram upados no servidor.
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


def files_by_type(type):
    """
    Essa função retorna todos os arquivos de uma extenção específica que foram upados no servidor.
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

