from flask import render_template, request, Blueprint

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/welcome')
def welcome():
    return render_template('welcome.html')