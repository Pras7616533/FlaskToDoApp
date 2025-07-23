import os
from flask import Flask

UPLOAD_FOLDER = os.path.join('static', 'uploads')

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your-secret-key'
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['UPLOAD_FOLDER'] = os.path.join(basedir, UPLOAD_FOLDER)
    
    from app.routes import main
    app.register_blueprint(main)

    return app
