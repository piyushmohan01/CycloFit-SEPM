import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail 
from cyclofit.config import Config

template_dir = os.path.abspath('../CycloFit/cyclofit/pages/templates')
static_dir = os.path.abspath('../CycloFit/cyclofit/pages/static')

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
mail = Mail()

def create_app(config_class=Config):
    app = Flask('__name__', template_folder=template_dir, static_folder=static_dir)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from cyclofit.users.routes import users
    from cyclofit.rides.routes import rides
    from cyclofit.main.routes import main

    app.register_blueprint(users)
    app.register_blueprint(rides)
    app.register_blueprint(main)

    return app