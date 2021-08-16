from flask import Flask
from app import views, kenzie

def create_app():
    app = Flask(__name__)

    views.init_app(app)
    kenzie.init_files(app)
        
    return app