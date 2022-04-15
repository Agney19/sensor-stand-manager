from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from threading import Thread
import os

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['UPLOAD_FOLDER'] = 'upload-files'
    #app.config['MAX_CONTENT_PATH'] = max size in bytes of files to be uploaded

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    def do():
        os.system("sudo picocom /dev/ttyACM0 --baud 115200 > log.txt")
    thread = Thread(target=do)
    thread.start()

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .reservation import reservation as reservation_blueprint
    app.register_blueprint(reservation_blueprint)

    from .test import test as test_blueprint
    app.register_blueprint(test_blueprint)

    from .audio import audio_bp as audio_blueprint
    app.register_blueprint(audio_blueprint)

    from .logs import logs_bp as logs_blueprint
    app.register_blueprint(logs_blueprint)

    return app
