import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail 

template_dir = os.path.abspath('../CycloFit/cyclofit/pages/templates')
static_dir = os.path.abspath('../CycloFit/cyclofit/pages/static')

app = Flask('__name__', template_folder=template_dir, static_folder=static_dir)
app.config['SECRET_KEY'] = os.environ.get('DB_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../CycloFit/cyclofit/database/main.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
mail = Mail(app)
from cyclofit.pages import routes