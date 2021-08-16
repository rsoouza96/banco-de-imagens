from app import views
from flask import Flask

def create_app():
    app = Flask(__name__)

    views.init_app(app)
        
    return app