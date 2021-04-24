import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

template_dir = os.path.abspath('../CycloFit/cyclofit/pages/templates')
static_dir = os.path.abspath('../CycloFit/cyclofit/pages/static')

app = Flask('__name__', template_folder=template_dir, static_folder=static_dir)
app.config['SECRET_KEY'] = 'fcff7fee5b3c64fc4aaf6f3b45422af2'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../CycloFit/cyclofit/database/users.db'
db = SQLAlchemy(app)

from cyclofit.pages import routes