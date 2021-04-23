from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask('__name__')
app.config['SECRET_KEY'] = 'fcff7fee5b3c64fc4aaf6f3b45422af2'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database/dir.db'
db = SQLAlchemy(app)

from cyclofit import routes