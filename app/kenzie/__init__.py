from flask import Flask
from .image import check_directory


def init_files(app: Flask):
    check_directory()