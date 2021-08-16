from flask import Blueprint
from ..kenzie.image import list_all_files, files_by_type


bp_files = Blueprint("bp_files", __name__)


@bp_files.route("/files")
def list_files():
    return list_all_files()


@bp_files.route("/files/<type>")
def list_files_by_type(type):
    return files_by_type(type)